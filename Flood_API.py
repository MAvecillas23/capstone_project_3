import requests

# FEMA API base URL
url = 'https://api.nationalflooddata.com/v3/data'
api_key = 'FEMA_API_KEY' # we need key 

def main():
    if api_key is None:
        print("API key not found! Please set the 'FEMA_API_KEY' environment variable.")
        return

    location = get_location()  # Get latitude and longitude from the user
    flood_data, error = get_flood_risk(location, api_key)
    
    if error:
        print('Sorry, could not get flood data.')
    else:
        flood_risk = evaluate_flood_risk(flood_data)
        print(f'The flood risk for the location ({location[0]}, {location[1]}) is: {flood_risk}')
        if flood_risk == 'High':
            print('It\'s not safe to live in this area.')
        else:
            print('The area is safe to live.')

def get_location():
    # Get user input for latitude and longitude
    lat = input('Enter the latitude: ').strip()
    long = input('Enter the longitude: ').strip()
    return lat, long

def get_flood_risk(location, api_key):
    lat, long = location
    headers = {'x-api-key': api_key}  # Required for FEMA API
    params = {
        'lat': lat,
        'long': long,
        'searchtype': 'addresscoord',  # Indicating it's a coordinate search
        'loma': False  # Request without LOMA (Letter of Map Amendment)
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for 400 or 500 errors
        data = response.json()  # Parse JSON response
        return data, None

    except Exception as ex:
        print(f"Error occurred: {ex}")
        print(response.text)  # Debugging info in case of failure
        return None, ex

def evaluate_flood_risk(flood_data):
    try:
        # Assuming the API returns some 'flood_risk' or similar value
        risk = flood_data.get('flood_risk', 'Unknown')

        if risk == 'High':
            return 'High'
        elif risk == 'Moderate':
            return 'Moderate'
        else:
            return 'Low'

    except KeyError:
        print('This data is not in the format expected')
        return 'Unknown'

if __name__ == '__main__':
    main()
