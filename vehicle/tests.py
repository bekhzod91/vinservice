# Django
from django.urls import reverse

# REST framework
from rest_framework.test import APITestCase
from rest_framework import status

# Project
from .utils import path_or, get_vehicle_by_vin, get_vehicle_property


class UtilsTest(APITestCase):
    def test_path_or(self):
        data = {
            'items': [
                {
                    'name': 'Mike'
                },
                {
                    'name': 'Katrina'
                }
            ]
        }

        self.assertEqual(path_or(data, ['items', 0, 'name']), 'Mike')
        self.assertEqual(path_or(data, ['items', 0, 'name1']), None)

        self.assertEqual(path_or(data, ['items', 1, 'name']), 'Katrina')
        self.assertEqual(path_or(data, ['items', 2, 'name']), None)

        self.assertEqual(path_or(data, ['items', 3, 'name'], 'Default'),
                         'Default')
        self.assertEqual(path_or([], ['items']), None)
        self.assertEqual(path_or({}, ['items']), None)

    def test_decodethis_get_key(self):
        vin = 'ZAMGJ45A390047326'
        vehicle = get_vehicle_by_vin(vin)

        year = get_vehicle_property(vehicle, 'Model Year')
        make = get_vehicle_property(vehicle, 'Make')
        model = get_vehicle_property(vehicle, 'Model')
        body_type = get_vehicle_property(vehicle, 'Body Style')
        color = get_vehicle_property(vehicle, 'Exterior Color')
        dimensions = get_vehicle_property(vehicle, 'Turning Diameter')
        weight = get_vehicle_property(vehicle, 'Curb Weight-automatic')

        self.assertEqual(year, '2009')
        self.assertEqual(make, 'Maserati')
        self.assertEqual(model, 'GranTurismo')
        self.assertEqual(body_type, 'COUPE 2-DR')
        self.assertEqual(color, '')
        self.assertEqual(dimensions, '35.10')
        self.assertEqual(weight, '4145')


class VinNumberTest(APITestCase):
    fixtures = ['vehicle.yaml']

    url = 'vehicle:vin'

    def test_vin_decodethis(self):
        url = reverse(self.url, kwargs={'vin': 'ZAMGJ45A390047326'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['vin'], 'ZAMGJ45A390047326')
        self.assertEqual(response.data['year'], '2009')
        self.assertEqual(response.data['make'], 'Maserati')
        self.assertEqual(response.data['model'], 'GranTurismo')
        self.assertEqual(response.data['type'], 'COUPE 2-DR')
        self.assertEqual(response.data['color'], '')
        self.assertEqual(response.data['dimensions'], '35.10')
        self.assertEqual(response.data['weight'], '4145')

    def test_vin_cache(self):
        url = reverse(self.url, kwargs={'vin': '1YVHP84DX55M13025'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['vin'], '1YVHP84DX55M13025')
        self.assertEqual(response.data['year'], '2005')
        self.assertEqual(response.data['make'], 'Mazda')
        self.assertEqual(response.data['model'], 'MAZDA6')
        self.assertEqual(response.data['type'], 'HATCHBACK 4-DR')
        self.assertEqual(response.data['color'], 'Red')
        self.assertEqual(response.data['dimensions'], '38.70')
        self.assertEqual(response.data['weight'], '3455')

    def test_vin_not_found(self):
        url = reverse(self.url, kwargs={'vin': '1YVHP84DX55M13026'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
