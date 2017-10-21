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

    # 2.  Use foursquare API to find a nearby restaurant with the latitude,
    # longitude, and mealType strings.
    # HINT: format for url will be something like
    # https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID
    # &client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi

    url = "https://api.foursquare.com/v2/venues/search?" \
          "client_id={0}&client_secret={1}&v={2}&ll={3},{4}&query={5}".format(
        foursquare_client_id, foursquare_client_secret, foursquare_v, coord[0],
        coord[1], mealType)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # 3. Grab the first restaurant

    restaurant = (result['response']['venues'][0])

    # 4. Get a  300x300 picture of the restaurant using the venue_id (you can
    # change this by altering the 300x300 value in the URL or replacing it with
    # 'orginal' to get the original picture

    url = "https://api.foursquare.com/v2/venues/{0}/photos?client_id={1}&" \
          "client_secret={2}&v={3}".format(restaurant['id'],
                                           foursquare_client_id,
                                           foursquare_client_secret,
                                           foursquare_v)
    h_photo = httplib2.Http()


    # 5. Grab the first image

    result_photo = json.loads(h_photo.request(url, 'GET')[1])

    r_name = restaurant['name']
    r_address = ''
    try:
        lines = restaurant['location']['formattedAddress']
        for l in lines:
            r_address += l + ' '

    except:
        r_address = "Unknown"

    # 6. If no image is available, insert default a image url

    try:
        prefix = (result_photo['response']['photos']['items'][0]['prefix'])
        suffix = (result_photo['response']['photos']['items'][0]['suffix'])
        r_img = prefix + '300x300' + suffix
    except:
        r_img = "http://pixabay.com/get/8926af5eb597ca51ca4c" \
                   "/1433440765/cheeseburger-34314_1280.png?direct"

    # 7. Return a dictionary containing the restaurant name, address, and image
    # url
    print ('Name: ' + r_name)
    print ('Address: ' + r_address)
    print ('Image: ' + r_img)
    return {'name': r_name, 'address': r_address, 'image': r_img}




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
