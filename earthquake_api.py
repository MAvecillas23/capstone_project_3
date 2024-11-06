""" This module calls the USGS api to get a list of earthquakes from a specific location """

import requests
from datetime import datetime

class EarthquakeAPIError(Exception):
    """Raised when requests made to the earthquake API are unsuccessful."""

    def __init__(self, msg):
        self.msg = msg


def earthquake_main(latitude, longitude):
    """ All earthquake_api functions are called from here.
        app.py will call this function with latitude and longitude coordinates
        Returns a list of earthquake string information back to app.py"""

    # query url with appropriate latitude and longitude parameters
    # url is also querying for all earthquake data in the last 3 years in a 15 mile (24km) radius
    earthquake_url = (f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson'
                      f'&starttime=2021-01-01'
                      f'&endtime=now'
                      f'&latitude={latitude}'
                      f'&longitude={longitude}'
                      f'&maxradiuskm=24'
                      f'&minmagnitude=3.0')

    # send to function to make api request return json data
    earthquake_json = earthquake_data_request(earthquake_url)

    # send to function to get specific data from json return list of earthquake
    # locations, dates, magnitudes
    earthquake_list = location_magnitude_date(earthquake_json)

    # for testing. Prints earthquake list
    display_earthquake_data(earthquake_list)

    # return earthquake_list back to app.py
    return earthquake_list


def earthquake_data_request(url):
    """ makes api request.
        returns all of locations earthquake json data."""

    earthquake_request = requests.get(url) # api request
    try:
        earthquake_request.raise_for_status()  # checks for http errors. raises error if there is
    except requests.HTTPError:
        raise EarthquakeAPIError("Error retrieving earthquake data.") # error message

    # convert earthquake_request to json data
    earthquake_json = earthquake_request.json()
    return earthquake_json


def location_magnitude_date(json_data):
    """ From json data, get only all location, milliseconds of earthquake date (converted to datetime)
        and magnitude data and append that information to a list.
        Return said list """

    magnitude_location_date_list = []

    # if no data is returned from json, raise error with message
    if json_data["metadata"]["count"] < 1 or not json_data:
        raise EarthquakeAPIError("No earthquake data available.")
    list_of_earthquakes = json_data['features']

    # get location, date, and magnitude of all earthquakes. Append to list.
    for earthquake in list_of_earthquakes:
        wanted_data = earthquake['properties']
        location = wanted_data['place']
        time = wanted_data['time']
        date = datetime.fromtimestamp(time / 1000).date()
        magnitude = wanted_data['mag']
        magnitude_location_date_list.append(f'{location} | Earthquake Date: {date} | Magnitude: {magnitude}')

    # return
    return magnitude_location_date_list


def display_earthquake_data(earthquake_list):
    """ This function is ONLY for test purposes. Prints the earthquake list.
        This ensures api works and data is being returned """
    if not earthquake_list:
        print(f'There are no earthquakes in this location.')
    else:
        for earthquake in earthquake_list:
            print(earthquake)

