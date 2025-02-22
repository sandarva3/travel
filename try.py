import requests
from key import mapKey
import json

def get_nearby_places(latitude, longitude):
    radius = 5000
    place_type = "tourist_attraction"
    
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&type={place_type}&key={mapKey}"
    
    try:
        response = requests.get(url, timeout=7)  # Added timeout to prevent long delays
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        
        # Parse the JSON response
        places_data = response.json() 
        
        return places_data  # Return the parsed JSON
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Example Usage
user_data = {
    "latitude": 27.632740,
    "longitude": 85.3374,
    "accuracy": 5,
    "altitude": 1350,
    "timestamp": "2024-02-20T10:45:00Z",
    "provider": "gps"
}

# Extract only required data
latitude = user_data["latitude"]
longitude = user_data["longitude"]

places = get_nearby_places(latitude, longitude)

if places:
    with open("output.json", "w") as file:
        json.dump(places, file)
    print("written to a file")
    #print(json.dumps(places, indent=2))  # Print the formatted JSON response
else:
    print("No places found or there was an error.")
