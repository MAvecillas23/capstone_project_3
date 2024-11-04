import requests
import geocoder
import main 
import os
from pprint import pprint

# FEMA API base URL
url = 'https://api.nationalflooddata.com/v3/data'
api_key = os.environ.get('FEMA_API_KEY')


class FloodAPIError(Exception):
    """Raised when requests made to the flood API are unsuccessful."""

    def __init__(self, msg):
        self.msg = msg


def get_flood_risk(lat, lng):
    """ Raises Flood_APIError, HTTPError, KeyError, IndexError  """
    data = make_request(lat, lng)
    if not data:
        raise FloodAPIError("Unable to retrieve flood risk data")
    return get_risk_from_json(data)


def get_risk_from_json(json):
    """ Extract relevant flood risk information from the JSON response
Raises KeyError and IndexError """
    flood_zones = json['result']['flood.s_fld_haz_ar']
    # Check the flood zone
    risk_levels = [zone['fld_zone'] for zone in flood_zones]
    if 'A' in risk_levels or 'V' in risk_levels:  # High-risk zones
        return 'NOT SAFE'
    elif 'X' in risk_levels:  # Low-risk zones
        return 'SAFE'
    else:
        return 'unknown flood risk'


def make_request(lat, lng):
    headers = {'x-api-key': api_key}  # Required for FEMA API

    params = {
        'lat': lat,
        'lng': lng,
        'searchtype': 'coord',
        'loma': False,
        'elevation': True
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an exception for 400 or 500 errors
    data = response.json()  # Parse JSON response
    return data

 