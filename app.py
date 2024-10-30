from flask import Flask, request, render_template
import geocoding as gc
import earthquake_api
import api_flood
import air_pollution_api
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
    lat, long = gc.getCoordinates(location)
    
    # earthquake_api section
    earthquake_info = earthquake_api.earthquake_main(lat, long)

    air_info = air_pollution_api.get_air_pollution([lat, long])
    
    flood_info = api_flood.get_flood_risk ( lat, long )
    
    return render_template('results.html',
                           earthquake_info=earthquake_info,
                           air_info=air_info,
                           Flood_info=flood_info)

if __name__ == "__main__":
    app.run()