from flask import Flask, request, render_template
import copy
import geocoding as gc
import earthquake_api
import api_flood
import air_pollution_api
import db
# import apis and db module here

# initialize Flask app object
app = Flask(__name__)

""" This class stores all api results data to save to database along with location"""
class DataStore():
    location = None
    earthquake = None
    aqi = None
    flood = None

global_data = DataStore()

# homepage
@app.route("/")
def index():
    return render_template("index.html")

# for the  results page
@app.route("/get-data")
def get_all_data():
    # get coordinates using the inputted city, state
    location = request.args.get('location')

    # convert location to coordinates. if unsuccessful direct user to the error page
    try:
        lat, long = gc.getCoordinates(location)
    except gc.LocationNotFoundError:
        return render_template("error.html", error_msg="Location not found.")

    """ call the earthquake_api module.
        returns a list of earthquakes or if no earthquakes exists display message.
        if api call raises an error, display error message. """
    try:
        earthquake_info = earthquake_api.earthquake_main(lat, long)
    except earthquake_api.EarthquakeAPIError as e:
        earthquake_info = [e.msg]

    """call the air_pollution_api module.
       returns an AQI index number
       if api call raises an error, display error message"""
    try:
        air_info = air_pollution_api.get_air_pollution([lat, long])
    except air_pollution_api.AirPollutionAPIError:
        air_info = "Unable to fetch air pollution data."

    """call the flood_api module.
       returns flood risk.
       if api call raises an error, display error message"""
    try:
        flood_info = api_flood.get_flood_risk(lat, long)
    except api_flood.FloodAPIError:
        flood_info = "Unable to retrieve flood risk data."

    # save location, earthquake, air pollution, and flood data to DataStore object
    global_data.location = copy.deepcopy(location)
    global_data.earthquake = copy.deepcopy(earthquake_info)
    global_data.aqi = copy.deepcopy(air_info)
    global_data.flood = copy.deepcopy(flood_info)

    return render_template('results.html',
                           earthquake_info=earthquake_info,
                           air_info=air_info,
                           Flood_info=flood_info)


# accesses the bookmarks page and talks with the app.db database to display
# data and ask user to enter an id to see more data
@app.route("/bookmarks")
def get_bookmarks_data():
    # this list will hold id, location, and date saved so user can decide which saved entry to get more info on
    db_list = db.display_id_location()

    """ if id number is valid get info from database that matches that id and display it to user.
        if id number isn't valid, redirect user to the error page"""
    if request.args:
        entry_id = int(request.args.get('id'))
        try:
            entry = db.get_api_info(entry_id)
        except:
            # this except is bare because we couldn't figure out what the exact
            # name of the exception was, so we couldn't import it
            # (throws error "db.ResultsDoesNotExist" [is that even real?])
            return render_template("error.html", error_msg=f"No results found with ID: {entry_id}")
    else:
        entry = None

    return render_template('bookmarks.html', db_list=db_list, entry=entry)

""" Save respective api data to the database """
@app.route("/save-results")
def save_results():

    db.save_api_info(global_data.location, global_data.earthquake, global_data.aqi, global_data.flood)
    db_list = db.display_id_location()
    return render_template('bookmarks.html', db_list=db_list, entry=None)


if __name__ == "__main__":
    app.run()
