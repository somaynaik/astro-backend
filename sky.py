from skyfield.api import load, Topos
from datetime import datetime

# Load timescale and current time
ts = load.timescale()
t = ts.now()

# Load planetary data (this downloads once, then caches)
planets = load('de421.bsp')

earth = planets['earth']

# Your location: Goa Engineering College
location = earth + Topos('15.4226 N', '73.9798 E')

# Planets + Moon + Sun
objects = {
    'Mercury': 'mercury',
    'Venus': 'venus',
    'Mars': 'mars',
    'Jupiter': 'jupiter barycenter',
    'Saturn': 'saturn barycenter',
    'Moon': 'moon',
    'Sun': 'sun'
}

print("\n🌌 Sky Report for GEC \n")
print("Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\n")

for name, key in objects.items():
    obj = planets[key]
    
    astrometric = location.at(t).observe(obj)
    alt, az, distance = astrometric.apparent().altaz()
    
    altitude = alt.degrees
    azimuth = az.degrees
    
    if altitude > 0:
        visibility = "VISIBLE"
    else:
        visibility = "NOT VISIBLE"
    
    print(f"{name}")
    print(f"  Altitude : {altitude:.2f}°")
    print(f"  Azimuth  : {azimuth:.2f}°")
    print(f"  Status   : {visibility}\n")