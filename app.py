from flask import Flask, request, render_template
import geocoding as gc
import api_flood 
# import apis and db module here

# initialize Flask app object
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get-data")
def get_all_data():
    location = request.args.get('location')
    lat, long = gc.getCoordinates(location)

    flood_info = api_flood.get_flood_risk ( lat, long )
    


    return render_template('results.html', Flood_info=flood_info)






if __name__ == "__main__":
    app.run()
