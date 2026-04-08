from flask import Flask, jsonify, request
from skyfield.api import load, Topos

app = Flask(__name__)

# Load data once
ts = load.timescale()
planets = load('de421.bsp')
earth = planets['earth']


def get_direction(az):
    if az >= 337.5 or az < 22.5:
        return "North"
    elif az < 67.5:
        return "North-East"
    elif az < 112.5:
        return "East"
    elif az < 157.5:
        return "South-East"
    elif az < 202.5:
        return "South"
    elif az < 247.5:
        return "South-West"
    elif az < 292.5:
        return "West"
    else:
        return "North-West"


@app.route("/")
def home():
    return "Sky API is running"


@app.route("/sky")
def sky():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    if lat is None or lon is None:
        return jsonify({"error": "Missing lat/lon"}), 400

    location = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
    t = ts.now()

    result = []

    planets_list = [
        ("Venus", "venus"),
        ("Mars", "mars"),
        ("Jupiter", "jupiter barycenter"),
        ("Saturn", "saturn barycenter")
    ]

    for name, key in planets_list:
        planet = planets[key]
        astrometric = location.at(t).observe(planet)
        alt, az, _ = astrometric.apparent().altaz()

        if alt.degrees > 0:
            result.append({
                "name": name,
                "direction": get_direction(az.degrees),
                "altitude": int(alt.degrees),
                "azimuth": int(az.degrees)
            })

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)