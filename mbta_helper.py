import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_Key = os.getenv("MBTA_API_KEY")

MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

def get_coords(place_name: str) -> tuple:
    """If the user inputs a location (i.e. name), they receive the coordoinates for their location"""
    query = urllib.parse.quote(place_name)
    url = f"{MAPBOX_BASE_URL}/{query}.json?access_token={MAPBOX_TOKEN}&limit=1" # Used ChatGPT for this line as code was not working during the debugging process

    with urllib.request.urlopen(url) as reponse:
        text_response = response.read().decode('utf-8')
        data = json.loads(text_response)
    
    coordinates = data["features"][0]["geometry"]["coordinates"]
    longitude, latitude = coordinates
    return coordinates

def closest_station(lat: float, lng: float) -> tuple:
    """Given user's coordinates, return 'station_name' and if station is wheelchair accessible"""
    
    url = (f"{MBTA_BASE_URL}?api_key={MBTA_API_KEY}"
       f"&filter[latitude]={latitude}&filter[longitude]={longitude}"
       f"&sort=distance")
    
    with urllib.request.urlopen(url) as response:
        response_text = response.read().decode('utf-8')
        data = json.loads(response_text)
    
    stop = data["data"][0]["attributes"]
    station_name = stop["name"]
    wheelchair_accessiblity = stop["wheelchair_boarding"]
    return station_name, wheelchair_accessiblity

    
    
def nearest_stop(place_name: str) -> tuple:
    """Find the nearest MBTA station based of the user's coordinates"""
    latitude, longitude = get_coords(place_name)
    station_name, wheelchair_accessiblity = closest_station(latitude, longitude)
    return station_name, wheelchair_accessiblity

if __name__ == "__main__":
    print(nearest_stop("Beacon Hill"))