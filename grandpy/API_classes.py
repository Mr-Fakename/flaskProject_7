import googlemaps
import requests
from grandpy.config import API_key


class GoogleMaps:
    def __init__(self):
        self.client = googlemaps.Client(key=API_key)

    def geocode(self, query):
        geocode_result = self.client.geocode(str(query))
        result_names = [location['long_name'] for location in geocode_result[0]['address_components'] if
                        any(x in ['locality', 'political', 'route'] for x in location['types'])]
        result_coordinates = geocode_result[0]['geometry']['location']
        return result_names, result_coordinates


class Wiki:
    def __init__(self, location, coordinates):
        self.url = "https://en.wikipedia.org/w/api.php"
        self.parameters = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "list": "geosearch",
            "titles": str(location),
            "exsentences": "10",
            "exlimit": "1",
            "exintro": 1,
            "explaintext": 1,
            "gscoord": str(coordinates['lat']) + "|" + str(coordinates['lng']),
            "gsradius": "1000",
            "gslimit": "1"
        }

    def wiki_query(self):
        response = requests.get(url=self.url, params=self.parameters)
        return response.json()
