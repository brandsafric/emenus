import httplib2
import json

def getGeoCodeLocation(inputString):
    google_api_key = "AIzaSyBsS-NTBxj2B291bJL-Tig9CrJo-OWmpMo"
    locationString = inputString.replace(" ", "+")
    url = "https://maps.googleapis.com/maps/api/geocode/json?" \
        "address={0}&key={1}".format(locationString, google_api_key)
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return (latitude,longitude)
    # print "response header: {0} \n \n".format(response)
