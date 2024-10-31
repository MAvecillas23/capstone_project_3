from flask import Flask, request, render_template
import geocoding as gc
import earthquake_api
import api_flood
import air_pollution_api
import requests
# import apis and db module here

# initialize Flask app object
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get-data")
def get_all_data():
    # get coordinates using input city, state
    location = request.args.get('location')

    try:
        lat, long = gc.getCoordinates(location)
    except gc.LocationNotFoundError:
        return render_template("error.html")

    try:
        earthquake_info = earthquake_api.earthquake_main(lat, long)
    except earthquake_api.EarthquakeAPIError as e:
        earthquake_info = [e.msg]

    try:
        air_info = air_pollution_api.get_air_pollution([lat, long])
    except air_pollution_api.AirPollutionAPIError:
        air_info = "Unable to fetch air pollution data."

    try:
        flood_info = api_flood.get_flood_risk(lat, long)
    except api_flood.FloodAPIError:
        flood_info = "Unable to retrieve flood risk data."

    return render_template('results.html',
                           earthquake_info=earthquake_info,
                           air_info=air_info,
                           Flood_info=flood_info)

if __name__ == "__main__":
    app.run()
