import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")  # FIXED capitalization

MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

def get_coords(place_name: str) -> tuple:
    """Given a place name, return (latitude, longitude) as floats."""
    query = urllib.parse.quote(place_name)
    url = f"{MAPBOX_BASE_URL}/{query}.json?access_token={MAPBOX_TOKEN}&limit=1"

    with urllib.request.urlopen(url) as response:  # FIXED typo
        text_response = response.read().decode('utf-8')
        data = json.loads(text_response)
    
    coordinates = data["features"][0]["geometry"]["coordinates"]
    longitude, latitude = coordinates
    return latitude, longitude  # FIXED order: lat first!

def closest_station(lat: float, lng: float) -> tuple:
    """Given user's coordinates, return (station_name, wheelchair_accessibility)."""
    url = (f"{MBTA_BASE_URL}?api_key={MBTA_API_KEY}"
           f"&filter[latitude]={lat}&filter[longitude]={lng}"
           f"&sort=distance")

    with urllib.request.urlopen(url) as response:
        response_text = response.read().decode('utf-8')
        data = json.loads(response_text)
    
    stop = data["data"][0]["attributes"]
    station_name = stop["name"]
    wheelchair_accessibility = stop["wheelchair_boarding"]  # FIXED spelling
    return station_name, wheelchair_accessibility

def nearest_stop(place_name: str) -> tuple:
    """Find the nearest MBTA station based on a place name."""
    latitude, longitude = get_coords(place_name)
    station_name, wheelchair_accessibility = closest_station(latitude, longitude)
    return station_name, wheelchair_accessibility

if __name__ == "__main__":
    print(nearest_stop("Beacon Hill"))
