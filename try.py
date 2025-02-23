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
        response = requests.get(url, timeout=7)  # Added timeout to prevent long delays
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        print("Map sent response.")
        
        # Parse the JSON response
        places = response.json() 
        num = 1
        places_detail = []
        print("Getting each place's relevant details.")
        for place in places["results"]:
            place_detail = {
                "placeNo": num,
                "place_id": place.get("place_id"),
                "address": place.get("vicinity"),
                "name":place.get("name"),
                "ratings": place.get("user_ratings_total", 0),
                "types": place.get("types"),
                "description": place.get("about")
            }
            places_detail.append(place_detail)
            num += 1
        print("Done")
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
        with open("output.json", "w") as file:
            json.dump(places, file, indent=3)
        print("written to a file.")
else:
    print("No places found or there was an error.")





'''

import requests
import json
from key import mapKey

def get_place_details(place_id):
    """ Fetch detailed place information using Google Maps Place Details API. """
    details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,editorial_summary,formatted_address,types,user_ratings_total,review&key={mapKey}"
    
    try:
        response = requests.get(details_url, timeout=7)
        response.raise_for_status()
        details_data = response.json()
        if "result" in details_data:
            return details_data["result"]
        return None
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch details for {place_id}: {e}")
        return None

def get_nearby_places(latitude, longitude):
    """ Fetch nearby tourist attractions and get detailed descriptions. """
    radius = 25000  # Increased radius to find better places
    place_type = "tourist_attraction"
    num = 1
    
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&type={place_type}&key={mapKey}"
    
    try:
        print("Fetching tourist attractions from Google Maps...")
        response = requests.get(url, timeout=7)
        response.raise_for_status()
        places_data = response.json()
        filtered_places = []

        if "results" in places_data:
            for place in places_data["results"]:
                place_id = place.get("place_id")
                name = place.get("name")
                ratings = place.get("user_ratings_total", 0)

                # Filter out places with less than 50 reviews (adjust as needed)
                if ratings < 200:
                    continue
                
                # Get more details
                details = get_place_details(place_id)
                if details:
                    place_info = {
                        "placeNo": num,
                        "name": details.get("name"),
                        "address": details.get("formatted_address"),
                        "description": details.get("editorial_summary", {}).get("overview", "No description available"),
                        "user_ratings": details.get("user_ratings_total", 0),
                        "types": details.get("types"),
                    }
                    num += 1
                    filtered_places.append(place_info)

        return filtered_places

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Example usage (Balkumari, Lalitpur, Nepal)
latitude = 27.6714861952194
longitude = 85.33868465233498

places = get_nearby_places(latitude, longitude)

if places:
    with open("output.json", "w", encoding="utf-8") as file:
        json.dump(places, file, indent=4, ensure_ascii=False)

    print("Places data saved to output.json")
else:
    print("No valid tourist attractions found.")

'''