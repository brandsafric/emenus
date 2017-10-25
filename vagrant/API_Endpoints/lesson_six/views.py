from findARestaurant import findARestaurant
from findARestaurant import getGeocodeLocation
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)



# foursquare_client_id = ''
foursquare_client_id = 'ZUPJOALYACXTHW3ZLE2I0RF2IWBOLFQPORW5LBUFHL2KEFTA'
# foursquare_client_secret = ''
foursquare_client_secret = 'S4M2PBBKJVQP3HM3SCKEZIIEJARLZ5ITP1KUKN4IXT03CXTM'
# google_api_key = ''
google_api_key = 'AIzaSyBsS-NTBxj2B291bJL-Tig9CrJo-OWmpMo'

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/restaurants', methods=['GET', 'POST'])
def all_restaurants_handler():
    if request.method == 'GET':
        # Call the method to Get all of the restaurants.
        return getAllRestaurants()
    elif request.method == 'POST':
        # Call the method to look up a new restaurant
        print "Creating new restaurant"
        location = request.args.get('location', '')
        mealType = request.args.get('mealType', '')
        newRestaurant = findARestaurant(mealType, location)
        # print (newRestaurant)
        restaurant = Restaurant(restaurant_name=newRestaurant['name'], restaurant_address=newRestaurant['address'], restaurant_image=newRestaurant['image'])
        # print restaurant
        session.add(restaurant)
        session.commit()
        return jsonify(Restaurant=restaurant.serialize)



def getAllRestaurants():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])

@app.route('/restaurants/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def restaurant_handler(id):
    try:
        restaurant = session.query(Restaurant).filter_by(id=id).one()
    except:
        print "no such restaurant"
        restaurant = "no such restaurant"
    if request.method == 'GET':
        print (restaurant)
        # return restaurant
        print(jsonify(Restaurant=restaurant.serialize))
        return jsonify(Restaurant=restaurant.serialize)
    elif request.method == 'PUT':
        try:
            # name = request.args.get('name', '')
            # location = request.args.get('location', '')
            # image = request.args.get('image', '')
            print ('restaurant updated')
            newRestaurant = Restaurant(restaurant_name=request.args.get('name', ''),
                                       restaurant_address=request.args.get('location', '')
                                       , restaurant_image=request.args.get('image', ''))
            print (newRestaurant)
            session.add(newRestaurant)
            session.commit()
            # return newRestaurant
            return jsonify(Restaurant=newRestaurant.serialize)
        except:
            print ("error in update.")
    elif request.method == 'DELETE':
        session.delete(restaurant)
        session.commit()
        print "restaurant deleted"
        return jsonify(Restaurant=restaurant.serialize)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)