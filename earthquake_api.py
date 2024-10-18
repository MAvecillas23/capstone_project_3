import requests
from main import main
from datetime import datetime


location_coordinates = main() # get geocoded coordinates from main.py
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

# where all functions get called from
def earthquake_main():
    earthquake_data, is_error = earthquake_data_request(earthquake_url)  # is_error checks if an error occurred is_error is true
                                                                        # if no error is_error is false
    # if an error was returned, then return the error message to wherever it was called
    if is_error:
        return earthquake_data
    # else get only the location, magnitude and date data
    else:
        get_wanted_data = location_magnitude_date(earthquake_data) # gets location, magnitude and date data from the earthquake json data
        display_earthquake_data(get_wanted_data)  # this function is for testing purposes only
        return get_wanted_data

# api call request
# returns all earthquake data
def earthquake_data_request(url):
    try:
        earthquake_request = requests.get(url).json()
        return earthquake_request, False  # return false if no errors occurred

    except:
        return 'Error: There was a problem accessing th USGS API.', True  # return true and error message if an error occurred



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
# **** This function is used for testing that earthquake data is being returned ***
def display_earthquake_data(needed_data):
    if not needed_data:
        print(f'There are no earthquakes at this location.')
    else:
        for earthquake in needed_data:
            print(earthquake)




if __name__ == '__main__':
    earthquake_main()