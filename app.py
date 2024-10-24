from flask import Flask, request, render_template
import geocoding as gc

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



    return render_template('scratch_results.html')






if __name__ == "__main__":
    app.run()
