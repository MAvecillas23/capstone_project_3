from flask import Flask, request, render_template
import geocoding as gc
import earthquake_api
import api_flood
import air_pollution_api
import db
import requests
# import apis and db module here

# initialize Flask app object
app = Flask(__name__)

stored_location = stored_aqi = stored_earthquake = stored_flood = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get-data")
def get_all_data():
    # get coordinates using input city, state
    location = request.args.get('location')

    try:
        lat, long = gc.getCoordinates(location)
        stored_location = location
    except gc.LocationNotFoundError:
        return render_template("error.html", error_msg="Location not found.")

    try:
        earthquake_info = earthquake_api.earthquake_main(lat, long)
        stored_earthquake = earthquake_info
    except earthquake_api.EarthquakeAPIError as e:
        earthquake_info = [e.msg]

    try:
        air_info = air_pollution_api.get_air_pollution([lat, long])
        stored_aqi = air_info
    except air_pollution_api.AirPollutionAPIError:
        air_info = "Unable to fetch air pollution data."

    try:
        flood_info = api_flood.get_flood_risk(lat, long)
        stored_flood = flood_info
    except api_flood.FloodAPIError:
        flood_info = "Unable to retrieve flood risk data."

    return render_template('results.html',
                           earthquake_info=earthquake_info,
                           air_info=air_info,
                           Flood_info=flood_info)


# accesses the bookmarks page and talks with the app.db database to display
# data and ask user to enter an id to see more data
@app.route("/bookmarks")
def get_bookmarks_data():
    db_list = db.display_id_location()

    if request.args:
        entry_id = int(request.args.get('id'))
        try:
            entry = db.get_api_info(entry_id)
        except:
            return render_template("error.html", error_msg=f"No results found with id {entry_id}")
    else:
        entry = None

    return render_template('bookmarks.html', db_list=db_list, entry=entry)


@app.route("/save-results")
def save_results():
    db.save_api_info(stored_location, stored_earthquake, stored_aqi, stored_flood)
    db_list = db.display_id_location()
    return render_template('bookmarks.html', db_list=db_list, entry=None)


if __name__ == "__main__":
    app.run()
