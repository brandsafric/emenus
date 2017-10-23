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
        print "Looking up a New restaurant"
        location = request.args.get('location', '')
        mealType = request.args.get('mealType', '')
        print location
        print mealType
        geolocation = getGeocodeLocation(location)
        print geolocation

        return findARestaurant(mealType, geolocation)


# YOUR CODE HERE

def getAllRestaurants():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])

@app.route('/restaurants/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def restaurant_handler(id):
    if id:
        return 'none'


# YOUR CODE HERE

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)