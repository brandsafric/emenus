from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "ZUPJOALYACXTHW3ZLE2I0RF2IWBOLFQPORW5LBUFHL2KEFTA"
foursquare_client_secret = "S4M2PBBKJVQP3HM3SCKEZIIEJARLZ5ITP1KUKN4IXT03CXTM"
foursquare_v = "20130815"


def findARestaurant(mealType, location):


# 1. Use getGeocodeLocation to get the latitude and longitude coordinates of
#  the location string.

    coord = getGeocodeLocation(location)
    print coord[0], coord[1]


# 2.  Use foursquare API to find a nearby restaurant with the latitude,
# longitude, and mealType strings.
# HINT: format for url will be something like
# https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID
# &client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi

    # coordString = coord.replace(" ", "+")
    url = "https://api.foursquare.com/v2/venues/search?" \
          "client_id={0}&client_secret={1}&v={2}&ll={3},{4}&query={5}".format(
        foursquare_client_id, foursquare_client_secret, foursquare_v, coord[0], coord[1], mealType)
    # print url
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # print(result['response']['venues'][0])


# 3. Grab the first restaurant

    name = (result['response']['venues'][0]['name'])
    print name

# 4. Get a  300x300 picture of the restaurant using the venue_id (you can
# change this by altering the 300x300 value in the URL or replacing it with
# 'orginal' to get the original picture
# 5. Grab the first image
# 6. If no image is available, insert default a image url
# 7. Return a dictionary containing the restaurant name, address, and image
# url
if __name__ == '__main__':
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland")
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney Australia")
