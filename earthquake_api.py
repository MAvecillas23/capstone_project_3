import requests
from datetime import datetime
import geocoding as gc


class EarthquakeAPIError(Exception):
    """Raised when requests made to the earthquake API are unsuccessful."""

    def __init__(self, msg):
        self.msg = msg


# where all functions get called from
# earthquake_main should be called from app.py with latitude and longitude coordinates
def earthquake_main(latitude, longitude):

    # query url with appropriate latitude and longitude parameters
    # url is also querying for all earthquake data in the last 3 years in a 15 mile radius
    earthquake_url = (f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson'
                      f'&starttime=2021-01-01'
                      f'&endtime=now'
                      f'&latitude={latitude}'
                      f'&longitude={longitude}'
                      f'&maxradiuskm=24'
                      f'&minmagnitude=3.0')


    earthquake_data = earthquake_data_request(earthquake_url)  # send url for earthquake api request
    # if api returned json data, get location, magnitude, and date of each earthquake
    get_wanted_data = location_magnitude_date(earthquake_data)
    display_earthquake_data(get_wanted_data)
    return get_wanted_data

# api call request
# returns all earthquake data
def earthquake_data_request(url):
    earthquake_request = requests.get(url) # make url request
    try:
        earthquake_request.raise_for_status()  # checks that there are no http errors...raises an error if there is...
    except requests.HTTPError:
        raise EarthquakeAPIError("Error retrieving earthquake data.")
    earthquake_json = earthquake_request.json()  # convert earthquake request to json data
    # errors are handled in app.py
    return earthquake_json

# gets only the earthquake location, magnitude and converted datetime date and puts
# that data in a list that is returned
def location_magnitude_date(data):
    magnitude_location_date_list = []

    if data["metadata"]["count"] < 1 or not data:
        raise EarthquakeAPIError("No earthquake data available.")
    list_of_earthquakes = data['features']

    for earthquake in list_of_earthquakes:
        wanted_data = earthquake['properties']
        location = wanted_data['place']
        time = wanted_data['time']
        date = datetime.fromtimestamp(time / 1000).date()
        magnitude = wanted_data['mag']
        magnitude_location_date_list.append(f'Location: {location} Date: {date}Magnitude: {magnitude}')

    return magnitude_location_date_list

# displays the location, magnitude, data list data to the user
# this function is for testing purposes
def display_earthquake_data(needed_data):
    if not needed_data:
        print(f'There are no earthquakes in this location.')
    else:
        for earthquake in needed_data:
            print(earthquake)

