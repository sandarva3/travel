import requests
from key import mapKey
import json
import time

def get_nearby_places(latitude, longitude):
    radius = 100000
    place_type = "tourist_attraction"
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&type={place_type}&key={mapKey}"
    
    try:
        print("Sending request to map")
        response = requests.get(url, timeout=(5, 10))  # Added timeout to prevent long delays
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        print("Map sent response.")
        # Parse the JSON response
        places = response.json() 
        num = 1
        places_detail = []
        print("Getting each place's relevant details.")

        for place in places["results"]:
            if place.get("user_ratings_total", 0) < 200:
                continue

            # Fetch Place Details to get photo count
            place_id = place.get("place_id")
            details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=photos&key={mapKey}"
            details_response = requests.get(details_url, timeout=(5, 10))
            details_response.raise_for_status()
            details = details_response.json()

            # Extract photo count
            photo_count = len(details.get("result", {}).get("photos", [])) if details.get("result", {}).get("photos") else 0

            # Add place details
            place_detail = {
                "placeNo": num,
                "place_id": place_id,
                "address": place.get("vicinity"),
                "name": place.get("name"),
                "ratings": place.get("user_ratings_total", 0),
                "types": place.get("types"),
                "description": place.get("vicinity"),
                "photo_count": photo_count  # Add photo count
            }
            places_detail.append(place_detail)
            num += 1

        print("Done")
        print(f"Total places after filter: {num}")
        return places_detail
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None



# Example Usage of: balkumari, lalitpur, Nepal
user_data = {
    "latitude": 27.6714861952194,
    "longitude": 85.33868465233498,
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
        with open("filtered_places.json", "w") as file:
            json.dump(places, file, indent=3)
        print("written to a file.")
else:
    print("No places found or there was an error.")
