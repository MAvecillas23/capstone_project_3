import geocoding as gc


def main():
    location = input('Please enter location you would like data on (city, state): ')
    coordinates = gc.getCoordinates(location)
    print(coordinates)  # testing
    return coordinates

if __name__ == '__main__':
    main()
