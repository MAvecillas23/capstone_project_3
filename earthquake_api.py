import requests
from datetime import datetime
import geocoding as gc


# where all functions get called from
def earthquake_main(location):
    print(location)
    location_coordinates = gc.getCoordinates(location) # get geocoded coordinates from main.py
    latitude = location_coordinates[0] # get latitude
    longitude = location_coordinates[1] # get longitude

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
    # if earthquake api didn't return anything, return none
    if earthquake_data is None:
        return None
    # if api returned json data, get location, magnitude, and date of each earthquake
    else:
        get_wanted_data = location_magnitude_date(earthquake_data)
        display_earthquake_data(get_wanted_data)
        return get_wanted_data

# api call request
# returns all earthquake data
def earthquake_data_request(url):
    earthquake_request = requests.get(url).json()
    earthquake_request.raise_for_status()  # checks that there are no http errors...raises an error if there is...
    # errors are handled in app.py
    return earthquake_request

# gets only the earthquake location, magnitude and converted datetime date and puts
# that data in a list that is returned
def location_magnitude_date(data):
    magnitude_location_date_list = []

    list_of_earthquakes = data['features']

    for earthquake in list_of_earthquakes:
        wanted_data = earthquake['properties']
        location = wanted_data['place']
        time = wanted_data['time']
        date = datetime.fromtimestamp(time / 1000).date()
        magnitude = wanted_data['mag']
        magnitude_location_date_list.append(f'Location: {location} *** Date: {date} *** Magnitude: {magnitude}')

    return magnitude_location_date_list

# displays the location, magnitude, data list data to the user
# this function is for testing purposes
def display_earthquake_data(needed_data):
    if not needed_data:
        print(f'There are no earthquakes in this location.')
    else:
        for earthquake in needed_data:
            print(earthquake)

