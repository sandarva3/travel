import requests
import json

def start():
    saved_places = requests.get("http://127.0.0.1:8000/allPlaces")
    json_saved_places = json.dumps(saved_places.json(), indent=3)
    print(json_saved_places)

start()