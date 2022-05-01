import requests
import urllib.parse, urllib.request

from config import *

class GoogleMapsClient():

    def __init__(self):
        self.key = GOOGLE_MAPS_KEY

    
    def get_static_image_url(self, location, width=1000, height=800):
        """Returns the url of a static Street View image.

        :param location: text string (such as "Chagrin Falls, OH") or a lat/lng value ("40.457375,-80.009353")
        :type location: str
        :param width: width of the returned image, defaults to 600
        :type width: int, optional
        :param height: height of the returned image, defaults to 400
        :type height: int, optional
        :return: url of the static Street View image.
        :rtype: str
        """
        base_url='https://maps.googleapis.com/maps/api/streetview?'

        params = {'location':location, 'size':str(width)+'x'+str(height), 'key':self.key}
        url = base_url+urllib.parse.urlencode(params)

        return url

    
    def get_geographic_coordinates(self,address):
        """Convert address into geographic coordinates.

        :param address: street address or plus code (like street addresses for people or places that don’t have one).
        :type address: str
        :return: dictionary that includes the location coordinates, and the coordinates for the northeast and the southwest wiewports. 
            The dictionary has the following format:
                >>> {
                        "location": {
                                "lat": 37.4224428,
                                "lng": -122.0842467
                            }, 
                        "viewport_northeast": {
                                "lat": 37.4239627802915,
                                "lng": -122.0829089197085
                            },
                        "viewport_southwest": {
                                "lat": 37.4212648197085,
                                "lng": -122.0856068802915
                            }
                    }
        :rtype: dict
        """
        base_url="https://maps.googleapis.com/maps/api/geocode/json?"

        params = {'address':address, 'key':self.key}
        url = base_url+urllib.parse.urlencode(params)

        r = requests.get(url).json()

        r_dict = {}
        try:
            r_dict['location'] = r['results'][0]['geometry']['location']
        except:
            pass
        try:
            r_dict['viewport_northeast'] = r['results'][0]['geometry']['viewport']['northeast']
        except:
            pass
        try:
            r_dict['viewport_southwest'] = r['results'][0]['geometry']['viewport']['southwest']
        except:
            pass
        
        return r_dict

