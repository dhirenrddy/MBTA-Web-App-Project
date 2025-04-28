from flask import Flask, render_template, request
import mbta_helper

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index(): 
    return render_template("index.html")

@app.route("/nearest_mbta", methods=["POST"])
def nearest_mbta():
    place_name = request.form.get("place_name")
    if not place_name:
        return render_template("error.html", message="Please enter an adequate location")
    
    try: 
        station, wheelchair_accessible = mbta_helper.closest_station(place_name)
        return render_template("mbta_station.html", station=station, wheelchair_accessbile = wheelchair_accessible)
    except Exception as e:
        return render_template("error.html", message=str(e))

if __name__ == "__main__":
    app.run(debug=True)