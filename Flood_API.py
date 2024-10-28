import requests
import geocoder
import main 
import os
from pprint import pprint

# FEMA API base URL
url = 'https://api.nationalflooddata.com/v3/data'
api_key = 'gbs3EAV35B8unwSBrApij6l02MS8JHAR2AZb2wg2'  

def main():
    location = input("Please enter the location (city, state): ")
    
    def get_coordinates(location):
        g = geocoder.arcgis(location)
        if g.latlng is not None:
            return g.latlng  # Returns a list [latitude, longitude]
        else:
            raise ValueError(f"No coordinates found for location: {location}")

    def get_flood_risk(location):
        
        try:
            coordinates = get_coordinates(location)  # Get coordinates for the location
            data, error = make_request(coordinates)
            if data:
                flood_risk, error = get_risk_from_json(data)
                if flood_risk:
                    return flood_risk, None 
                else: 
                    return None, error 
            else:
                return None, error 
        except ValueError as ve:
            return None, str(ve)

    def get_risk_from_json(json):
        # Extract relevant flood risk information from the JSON response
        try:
            flood_zones = json['result']['flood.s_fld_haz_ar']
            if flood_zones:
                # Check the flood zone
                risk_levels = [zone['fld_zone'] for zone in flood_zones]
                if 'A' in risk_levels or 'V' in risk_levels:  # High-risk zones
                    return 'not safe', None
                elif 'X' in risk_levels:  # Low-risk zones
                    return 'safe', None
                else:
                    return 'unknown flood risk', None
            else:
                return 'No flood hazard areas found.', None
        except (KeyError, IndexError) as e:
            return None, str(e)

    def make_request(coordinates):
        headers = {'x-api-key': api_key}  # Required for FEMA API
        lat, lng = coordinates  

        params = {  
            'lat': lat,
            'lng': lng,
            'searchtype': 'coord',  
            'loma': False,
            'elevation': True
        } 

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raise an exception for 400 or 500 errors
            data = response.json()  # Parse JSON response
            return data, None

        except Exception as ex:
            print(f"Error occurred: {ex}")
            return None, ex

    flood_risk, error = get_flood_risk(location)
    if error:
        print(f"Error: {error}")
    else:
        print(f"The flood risk for {location} is: {flood_risk}")

if __name__ == '__main__':
    main()
