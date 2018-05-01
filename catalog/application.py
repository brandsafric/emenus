from flask import Flask, render_template, request, \
    redirect, url_for, flash, jsonify
from flask import session as login_session
from flask import make_response, send_from_directory
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from database_setup import Base, Restaurant, MenuItem, User, Picture
from functools import wraps
import random
import string
import httplib2
import json
import requests
import os

app = Flask(__name__, static_url_path="/var/www/emenus/static")

APP_PATH = '/var/www/emenus/'

CLIENT_ID = json.loads(
    open(APP_PATH + 'client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

# engine = create_engine('sqlite:///restaurantmenuwithusers.db')
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

UPLOAD_FOLDER = APP_PATH + 'static/img/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024


# Login Methods
# Create anti-forgery state token
@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Google Login/logout
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data

    try:
        # Upgrade the authorization code into a credential object
        oauth_flow = flow_from_clientsecrets(APP_PATH +
                                             'client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the '
                                            'authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={0}') \
        .format(access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intendedn
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match "
                                            "given user."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        # print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # stored_access_token = login_session.get('access_token')
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps("Current user is already "
                                            "connected."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later user.
    login_session['provider'] = 'google'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get User Info
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name'].title()
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if user exists, if not create a new one
    user_id = get_user_id(login_session['email'])

    if not user_id:
        user_id = create_user(login_session)

    login_session['user_id'] = user_id

    return user_login_message()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You are not allowed to access there.")
            return redirect('/login')

    return decorated_function


def user_login_message():
    output = '<div class="profileImg"><img src="' + login_session['picture'] \
             + ' "></div> ' + '<div class="welcomeMsg">' + 'Welcome, ' + \
             login_session['username'] + '!'

    flash("{0} has logged in.".format(login_session['username']))
    return output


def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')

    if access_token is None:
        response = make_response(
            json.dumps("Current user not connected."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Execute HTTP GET request to revoke current token.
    url = 'https://accounts.google.com/o/oauth2/revoke?token={0}' \
        .format(access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps("Successfully disconnected."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given '
                                            'user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# End Google Login/Logout
# DISCONNECT - Revoke a current user's token and reset their login session.
@app.route("/disconnect")
def disconnect():
    if 'provider' in login_session:
        username = login_session['username']
        if login_session['provider'] == 'google':
            gdisconnect()
        elif login_session['provider'] == 'facebook':
            fbdisconnect()

        del login_session['provider']
        flash("{0} has logged out.".format(username))
        return redirect(url_for('show_restaurants'))
    else:
        flash("You were not logged in to begin with!")
        return redirect(url_for('show_restaurants'))


# Facebook Login section
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = request.data
    app_id = json.loads(open(APP_PATH + 'fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(open(APP_PATH + 'fb_client_secrets.json',
                                 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=' \
          'fb_exchange_token&client_id={0}&client_secret={1}&' \
          'fb_exchange_token={2}'.format(app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    # strip expire tag from access token
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token={0}&' \
          'fields=name,id,email'.format(token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"].title()
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # # The token must be stored in the login_session in order to properly
    # logout, let's strip out the information before the equals sign
    #  in our token
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token={0}' \
          '&redirect=0&height=200&width=200'.format(token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = get_user_id(login_session['email'])

    if not user_id:
        user_id = create_user(login_session)

    login_session['user_id'] = user_id
    return user_login_message()


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    url = 'https://graph.facebook.com/{0}/permissions'.format(facebook_id)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['facebook_id']
    return "you have been logged out"


# End Facebook Login Section


# User Helper functions
def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception, e:
        return None


def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def create_user(login_session):
    # Check for the provider used to see if the directory exists
    if login_session['provider'] == 'google':
        user_id = login_session['gplus_id']
        directory = UPLOAD_FOLDER + login_session['gplus_id']
    else:
        user_id = login_session['facebook_id']
        directory = UPLOAD_FOLDER + login_session['facebook_id']
    if not os.path.exists(directory):
        os.makedirs(directory)
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'],
                   path=user_id)
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# End login methods


@app.route('/')
@app.route('/restaurants/')
def show_restaurants():
    restaurants = session.query(Restaurant).order_by(asc(Restaurant.name)) \
        .all()
    pictures = session.query(Picture).all()
    pics = [(p.id, p.path) for p in pictures]
    rests = [(r.id, r.name, r.picture_id, r.cuisine) for r in restaurants]
    rest_list = []
    for i, v in enumerate(rests):
        for x, y in enumerate(pics):
            if v[2] == y[0]:
                rest_list.append((v[0], v[1], y[1], v[3]))
    if 'username' not in login_session:
        return render_template('restaurants.min.html',
                               restaurants=rest_list),
    else:
        return render_template('restaurants.min.html',
                               restaurants=rest_list,
                               picture=login_session['picture'])


@app.route('/restaurants/new', methods=['GET', 'POST'])
@login_required
def create_restaurant():
    # Grab the user ID first
    user = get_user_info(login_session['user_id'])
    default_img = session.query(Picture).filter_by(id=1).one()
    if request.method == 'POST':
        try:
            # Get the path for the user
            newRestaurant = Restaurant(name=request.form['name'],
                                       picture_id=request.form['picture'],
                                       user_id=login_session['user_id'])
        except:
            try:
                newRestaurant = Restaurant(name=request.form['name'],
                                           picture_id=request.form['picture'],
                                           user_id=login_session['user_id'])
            except ValueError:
                print "error"

        session.add(newRestaurant)
        session.commit()
        flash("New Restaurant created by {0}!".format(
            login_session['username']))
        return redirect(url_for('show_restaurants'))
    else:
        user_pics = get_pictures()
        return render_template('newRestaurant.min.html',
                               picture=login_session['picture'],
                               user_pics=user_pics,
                               default_img=default_img)


def get_pictures():
    # Grab the user ID first
    user = get_user_info(login_session['user_id'])
    user_pics = session.query(Picture).filter_by(user_id=user.id).all()
    return user_pics


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_restaurant(restaurant_id):
    restaurantToEdit = session.query(Restaurant). \
        filter_by(id=restaurant_id).one()
    r_picture = session.query(Picture).filter_by(
        id=restaurantToEdit.picture_id).one()
    default_img = session.query(Picture).filter_by(id=1).one()
    user = get_user_info(login_session['user_id'])
    if restaurantToEdit.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not" \
               " authorized to edit this restaurant. Please create " \
               "your own restaurant in order to edit.');" \
               "window.location.href = '" + request.referrer + \
               "';}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        if request.form['name']:
            restaurantToEdit.name = request.form['name']
        # Get the path for the user
        user = get_user_info(restaurantToEdit.user_id)
        restaurantToEdit.picture_id = request.form['picture']
        flash("Restaurant has been edited by {0}."
              .format(login_session['username']))
        session.commit()
        return redirect(url_for('show_menu', restaurant_id=restaurant_id,
                                picture=login_session['picture']))
    else:
        user_pics = get_pictures()
        return render_template(
            'editRestaurant.min.html', restaurant_id=restaurant_id,
            restaurant=restaurantToEdit, picture=login_session['picture'],
            user_pics=user_pics, restaurant_pic=restaurantToEdit.picture,
            r_picture=r_picture, default_img=default_img)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_restaurant(restaurant_id):
    restaurantToDelete = session.query(Restaurant).filter_by(
        id=restaurant_id).one()
    r_picture = session.query(Picture).filter_by(
        id=restaurantToDelete.picture_id).one()
    itemsToDelete = session.query(MenuItem). \
        filter_by(restaurant_id=restaurant_id).all()
    if restaurantToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not" \
               " authorized to delete this restaurant. Please create " \
               "your own restaurant in order to edit.');" \
               "window.location.href = '" + request.referrer + \
               "';}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if itemsToDelete:
            for i in itemsToDelete:
                session.delete(i)
        session.delete(restaurantToDelete)
        session.commit()
        flash("Restaurant has been deleted by {0}".
              format(login_session['username']))

        json.dumps({'status': 'OK', 'index': restaurantToDelete.id,
                    'Deleted': 'yes'})
        return show_restaurants()
    else:
        return render_template('deleteRestaurant.min.html',
                               restaurant=restaurantToDelete,
                               r_picture=r_picture,
                               items=itemsToDelete,
                               picture=login_session['picture'])


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def show_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    creator = get_user_info(restaurant.user_id)
    appetizers = session.query(MenuItem).filter_by(restaurant_id=restaurant_id,
                                                   course="Appetizer").all()
    entrees = session.query(MenuItem).filter_by(restaurant_id=restaurant_id,
                                                course="Entree").all()
    desserts = session.query(MenuItem).filter_by(restaurant_id=restaurant_id,
                                                 course="Dessert").all()
    beverages = session.query(MenuItem).filter_by(restaurant_id=restaurant_id,
                                                  course="Beverage").all()
    picture = session.query(Picture).filter_by(id=restaurant.picture_id).one()
    if 'username' not in login_session:
        return render_template('showMenu.min.html', appetizers=appetizers,
                               entrees=entrees, desserts=desserts,
                               beverages=beverages, restaurant=restaurant,
                               creator=creator, r_picture=picture)
    else:
        return render_template('showMenu.min.html', restaurant=restaurant,
                               appetizers=appetizers, entrees=entrees,
                               desserts=desserts, beverages=beverages,
                               creator=creator,
                               picture=login_session['picture'],
                               r_picture=picture)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
@login_required
def create_menu_item(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if login_session['user_id'] != restaurant.user_id:
        return "<script>function myFunction() {alert('You are not" \
               "\ authorized to add menu items to this restaurant. " \
               "Please create your own restaurant in order to edit.');" \
               "window.location.href = '" + request.referrer + \
               "';}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'],
                           description=request.form['description'],
                           price=request.form['price'],
                           course=request.form['course'],
                           restaurant_id=restaurant_id,
                           user_id=restaurant.user_id)
        session.add(newItem)
        session.commit()
        flash("{0} created {1} for {2}!".format(
            login_session['username'], request.form['name'], restaurant.name))
        return redirect(url_for('show_menu', restaurant_id=restaurant_id,
                                picture=login_session['picture']))
    else:
        return render_template('newMenuItem.min.html',
                               restaurant=restaurant,
                               picture=login_session['picture'])


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
@login_required
def edit_menu_item(restaurant_id, menu_id):
    itemToEdit = session.query(MenuItem).filter_by(id=menu_id).one()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if login_session['user_id'] != restaurant.user_id:
        return "<script>function myFunction() {alert('You are not authorized" \
               " to edit menu items to this restaurant. Please create your" \
               " own restaurant in order to edit items.');window." \
               "location.href = '" + request.referrer + \
               "';}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        itemToEdit.name = request.form['name']
        itemToEdit.description = request.form['description']
        itemToEdit.price = request.form['price']
        itemToEdit.course = request.form['course']
        session.add(itemToEdit)
        flash("Menu Item has been edited by {0}.".
              format(login_session['username']))
        session.commit()
        return redirect(url_for('show_menu', restaurant_id=restaurant_id,
                                picture=login_session['picture']))
    else:
        return render_template('editMenuItem.min.html',
                               restaurant_id=restaurant_id, item=itemToEdit,
                               picture=login_session['picture'])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
@login_required
def delete_menu_item(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if login_session['user_id'] != restaurant.user_id:
        return "<script>function myFunction() {alert('You are not " \
               "authorized to delete menu items to this restaurant. " \
               "Please create your own restaurant in order to delete " \
               "items.');window.location.href = '" + request.referrer + \
               "';}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item has been deleted by {0}.".
              format(login_session['username']))
        return redirect(url_for('show_menu', restaurant_id=restaurant_id,
                                picture=login_session['picture']))
    else:
        return render_template(
            'deleteMenuItem.min.html', restaurant_id=restaurant_id,
            item=itemToDelete, picture=login_session['picture'])


# API Endpoints
@app.route('/restaurants/JSON')
def restaurant_json():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurant_item_json(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(items=[item.serialize])


# End API Endpoints

@app.route('/deleteImage', methods=['POST'])
def delete_image():
    data = request.get_json()
    index = int(data['image_index'])
    user = get_user_info(login_session['user_id'])
    try:
        # Need to reset any restaurants that have the image back to default
        # image
        restaurantsWithimages = session.query(Restaurant).filter_by(
            picture_id=index).all()
        for r in restaurantsWithimages:
            r.picture_id = 1
            session.commit()
    except Exception, e:
        print "error with locating other restaurants with that picture"
    try:
        pictureToDelete = session.query(Picture).filter_by(user_id=user.id,
                                                           id=index).one()
        session.delete(pictureToDelete)
        session.commit()
        f = os.path.join(app.config['UPLOAD_FOLDER'], user.path,
                         pictureToDelete.filename)
        if os.path.exists(f):
            try:
                os.remove(f)
                return json.dumps({'status': 'OK', 'index': "x", 'deleted':
                                   'yes', 'filename':
                                   pictureToDelete.filename})
            except OSError, e:
                print ("Error: {0} - {1}.".format(e.f, e.strerror))
                return json.dumps({'status': 'ERROR', 'index': "x",
                                   'deleted': 'no',
                                   'filename': pictureToDelete.filename,
                                   'picslocated': 'no'})
        else:
            print(
                "Sorry, I can not find {0} file in the filesystem.".format(f))
            return json.dumps(
                {'status': 'ERROR', 'index': "x", 'deleted': 'no',
                 'filename': pictureToDelete.filename,
                 'picslocated': 'no'})
    except Exception, e:
        print "error with removing file from DB"
        return json.dumps({'status': 'ERROR', 'index': index, 'deleted': 'no'})


@app.route('/uploadImage', methods=['POST'])
def upload_image():
    f = request.files['image']
    filename = f.filename
    user = get_user_info(login_session['user_id'])
    # Get the path for the user
    path = user.path
    destination = os.path.join(app.config['UPLOAD_FOLDER'], path, filename)
    fullpath = 'img/uploads/' + path + '/' + filename
    try:
        newPicture = Picture(filename=filename, path=fullpath, user_id=user.id)
        session.add(newPicture)
        session.commit()
        f.save(destination)
        return json.dumps(
            {'status': 'OK', 'index': newPicture.id, 'uploaded': 'yes',
             'filename': filename, 'path': fullpath})
    except Exception, e:
        print "Error. Could not save to database."
        return json.dumps(
            {'status': 'ERROR', 'index': "n/a", 'uploaded': 'no'})


if __name__ == '__main__':
    # Invalidate previous sessions by generating a unique key
    app.secret_key = os.urandom(32)
    app.debug = True
    app.run(host='0.0.0.0')
