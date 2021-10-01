import unittest
from unittest import mock

from grandpy import app
from grandpy.API_classes import GoogleMaps, Wiki
from grandpy.parser import parse


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    def setUp(self):
        app.config['TESTING'] = True

        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/')

        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.app.post(
            '/search',
            data=dict(
                input='Test input'
            ),
            content_type='application/json',
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 400)

    def test_query_cleanup(self):
        query = "this is a test query"

        self.assertEqual(parse(query), ["test", "query"])

    @staticmethod
    def mocked_requests(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(None, 404)

    @mock.patch('requests.get', side_effect=mocked_requests)
    def test_geocoding(self, mock_get):
        geocoding_mock = [{
            'address_components': [
                {
                    'long_name': 'Budel', 'short_name': 'Budel',
                    'types': ['locality', 'political']
                },
                {
                    'long_name': 'Cranendonck', 'short_name': 'Cranendonck',
                    'types': ['administrative_area_level_2', 'political']
                }
            ],
            'formatted_address': '6021 Budel, Netherlands',
            'geometry': {
                'location': {'lat': 51.2741027, 'lng': 5.5763506}
            }
        }]
        # Assert requests.get calls
        maps_client = GoogleMaps()
        json_data = maps_client.geocode('Budel')
        self.assertEqual(json_data, (['Budel', 'Cranendonck', 'North Brabant', 'Netherlands'],
                                     {'lat': 51.2741027, 'lng': 5.5763506}))

    def test_wiki_api(self):
        wiki_mock = mock.Mock(
            status_code=200,
            data={
                'batchcomplete': '',
                'query': {
                    'pages': {
                        '9420': {
                            'pageid': 9420,
                            'ns': 0,
                            'title': 'Eindhoven',
                            'extract': 'Eindhoven ( EYENT-hoh-vən, Dutch: [ˈɛintˌɦoːvə(n)] (listen)) is the '
                                       'fifth-largest '
                                       'city and a municipality of the Netherlands, located in the south of the '
                                       'country. '
                                       'It had a population of 231,469 in 2019, making it the largest city in the '
                                       'province of North Brabant. Eindhoven was originally located at the confluence '
                                       'of '
                                       'the Dommel and Gender.Neighbouring cities and towns include Son en Breugel, '
                                       'Nuenen, Geldrop-Mierlo, Helmond, Heeze-Leende, Waalre, Veldhoven, Eersel, '
                                       'Oirschot and Best. The agglomeration has a population of 337,'
                                       '487. The metropolitan area consists of 780,611 inhabitants. The city region '
                                       'has a '
                                       'population of 753,426. The Brabantse Stedenrij combined metropolitan area has '
                                       'about two million inhabitants.'
                        }
                    },
                    'geosearch': [
                        {'pageid': 1286975,
                         'ns': 0,
                         'title': 'Philips Stadion',
                         'lat': 51.44178055555555,
                         'lon': 5.467441666666667,
                         'dist': 158.8,
                         'primary': ''
                         }
                    ]
                }
            })
        # Assert requests.get calls
        get_response = mock.Mock(return_value=wiki_mock)
        wiki = Wiki('Eindhoven', {'lat': 51.4417805, 'lng': 5.4674416}).wiki_query()
        self.assertIn('9420', wiki['query']['pages'])


if __name__ == "__main__":
    unittest.main()
