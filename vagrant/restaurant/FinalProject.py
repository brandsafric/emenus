from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    # return 'This page will show all my restaurants.'
    # return render_template('restaurant.html', restaurants=restaurants, items=items)
    restaurants = session.query(Restaurant).all()
    return render_template('restaurant.html', restaurants=restaurants)

@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    # return "This page will be for making a new restaurant."
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash("New Restaurant created!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    # return "This page will be for editing restaurant {0}.".format(restaurant_id)
    # return render_template('editRestaurant.html', restaurant=restaurants[restaurant_id - 1])
    restaurantToEdit = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            restaurantToEdit.name = request.form['name']
        session.add(restaurantToEdit)
        flash("Restaurant has been edited")
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template(
            'editRestaurant.html', restaurant_id=restaurant_id, restaurant=restaurantToEdit)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    print 'here now'
    # return "This page will be for deleting {0}.".format(restaurant_id)
    # return render_template('deleteRestaurant.html', restaurant=restaurants[restaurant_id - 1])
    restaurantToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
    print 'here now 2'
    print restaurantToDelete
    if request.method == 'POST':
        print 'here'
        session.delete(restaurantToDelete)
        session.commit()
        flash("Restaurant has been deleted")
        return redirect(url_for('showRestaurants'))
    else:
        print 'not POST'
        return render_template('deleteRestaurant.html', restaurant=restaurantToDelete)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    # return "This page is the menu for restaurant {0}".format(restaurant_id)
    # return render_template('showMenu.html', restaurant=restaurants[restaurant_id - 1], items=items)
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('showMenu.html', restaurant=restaurant, items=items, restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    # return "This page is for making a new menu item for restaurant {0}.".format(restaurant_id)
    # return render_template('newMenuItem.html', restaurant=restaurants[restaurant_id - 1])
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New Item created!")
        return redirect(url_for('showRestaurants'))
    else:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template('newMenuItem.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    # return "This page is forf editing menu item {0}.".format(menu_id)
    # return render_template('editMenuItem.html', restaurant=restaurants[restaurant_id - 1], item=items[menu_id - 1])
    if request.method == 'POST':
        print "here"
        print restaurant_id
        print menu_id
        print request.form['name']
        editedItem = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'])
        print editedItem
        session.add(editedItem)
        flash("Menu Item has been edited")
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        itemToEdit = session.query(MenuItem).filter_by(id=menu_id).one()
        return render_template('editMenuItem.html', restaurant_id=restaurant_id, item=itemToEdit)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    # return "This page is for deleting menu item {0}.".format(menu_id)
    # return render_template('deleteMenuItem.html', restaurant=restaurants[restaurant_id -1], item=items[menu_id - 1])
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        print 'here'
        session.delete(itemToDelete)
        session.commit()
        flash("Item has been deleted")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template(
            'deleteMenuItem.html', restaurant_id=restaurant_id, item=itemToDelete)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

