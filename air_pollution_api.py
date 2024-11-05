import requests
import os


class AirPollutionAPIError(Exception):
    """Raised when requests made to the air pollution API are unsuccessful."""

    def __init__(self, msg):
        self.msg = msg


def get_air_pollution(coordinates: list) -> int:
    """
    Returns the Air Quality Index for a given set of coordinates from
    OpenWeatherMap's data set.

    Args:
        coords (list): The latitude and longitude (respectively) of a given
            location.

    Returns:
        int: The location's Air Quality Index.

    Raises:
        AirPollutionAPIError: If the HTTP request was unsuccessful.
    """

    endpoint = "http://api.openweathermap.org/data/2.5/air_pollution"
    try:
        payload = {
            "lat": coordinates[0],
            "lon": coordinates[1],
            "appid": os.environ["OWM_API_KEY"],
        }
    except KeyError:
        print("ERROR: OWM_API_KEY not set")  # logs to console
        raise AirPollutionAPIError("Unable to set request parameters. Did you set OWM_API_KEY?")

    response = requests.get(endpoint, params=payload)

    # will raise an HTTPError if the request was unsuccessful
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        raise AirPollutionAPIError(f"Unable to fetch air quality data: {e.strerror}")

    return response.json()["list"][0]["main"]["aqi"]
