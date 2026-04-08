import tkinter as tk
from skyfield.api import load, Topos
import geocoder
import speech_recognition as sr
import pyttsx3
import threading

# -----------------------------
# Voice Engine (JARVIS)
# -----------------------------
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# -----------------------------
# Get location
# -----------------------------
g = geocoder.ip('me')

if g.latlng is None:
    lat, lon = 15.4226, 73.9798
else:
    lat, lon = g.latlng

# -----------------------------
# Sky setup
# -----------------------------
ts = load.timescale()
planets = load('de421.bsp')
earth = planets['earth']

location = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)

# -----------------------------
# Direction logic
# -----------------------------
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

# -----------------------------
# Sky logic
# -----------------------------
def get_sky_info():
    t = ts.now()
    result = ""

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
            direction = get_direction(az.degrees)
            result += f"{name}: Look {direction}, {int(alt.degrees)} degrees up.\n"

    return result if result else "No major planets visible right now."

# -----------------------------
# Voice command listener
# -----------------------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        return command
    except:
        return ""

# -----------------------------
# Handle commands
# -----------------------------
def jarvis():
    while True:
        command = listen()

        if "where" in command or "sky" in command:
            info = get_sky_info()
            output.insert(tk.END, info + "\n")
            speak(info)

        elif "location" in command:
            msg = f"You are at latitude {lat:.2f} longitude {lon:.2f}"
            output.insert(tk.END, msg + "\n")
            speak(msg)

        elif "exit" in command or "stop" in command:
            speak("Goodbye")
            break

# -----------------------------
# UI
# -----------------------------
root = tk.Tk()
root.title("JARVIS Sky Assistant")
root.geometry("500x500")

title = tk.Label(root, text="🌌 JARVIS Sky Assistant", font=("Arial", 16))
title.pack(pady=10)

output = tk.Text(root, height=20, width=60)
output.pack(pady=10)

btn = tk.Button(root, text="Start JARVIS", command=lambda: threading.Thread(target=jarvis).start())
btn.pack(pady=10)

root.mainloop()