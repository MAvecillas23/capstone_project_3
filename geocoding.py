import geocoder


class LocationNotFoundError(Exception):
    """Geocoding error class. Raised when a location's coordinates aren't found."""

    def __init__(self, msg):
        self.msg = msg


def getCoordinates(location: str) -> list:
    """
    Accepts the name of a location and returns its coordinates.

    Args:
        location (str): The location to be geocoded.

    Returns:
        list: A list containing the latitude and longitude (respectively) of
            the location in question.

    Raises:
        LocationNotFoundError: If no correspondent coordinates are found for
            the given location.
    """
    get_data = geocoder.arcgis(location)
    coordinates = get_data.latlng
    if coordinates is not None:
        return coordinates
    else:
        raise LocationNotFoundError(f'No coordinates found for location "{location}".')
