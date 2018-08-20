import requests
from django.conf import settings

GET_VEHICLE_DATA_API = 'https://www.decodethis.com' \
                       '/webservices/decodes' \
                       '/%(vin)s/%(key)s/1.json'


def path_or(items, keys, default=None):
    key = keys[0]
    odd_keys = keys[1:]

    if type(items) == list and type(key) == int:
        try:
            if odd_keys:
                return path_or(items[key], odd_keys, default)
            else:
                return items[key]
        except IndexError:
            pass

    if type(items) == dict and type(key) == str:
        try:
            if odd_keys:
                return path_or(items.get(key), odd_keys, default)
            else:
                return items.get(key)
        except IndexError:
            pass

    return default


def get_vehicle_by_vin(vin):
    url = GET_VEHICLE_DATA_API % {
        'vin': vin,
        'key': settings.DECODE_THIS_API_KEY
    }

    try:
        data = requests.get(url)
        return data.json()
    except requests.HTTPError:
        return None


def get_vehicle_property(data, key):
    vehicle = path_or(data, ['decode', 'vehicle', 0, 'Equip'], [])
    keys = filter(lambda item: item.get('name') == key, vehicle)

    return path_or(list(keys), [0, 'value'], '')
