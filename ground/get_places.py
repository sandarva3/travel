import requests
from key import mapKey
import json
import time




def get_nearby_places(latitude, longitude):
    radius = 20000
    place_type = "tourist_attraction"
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&type={place_type}&key={mapKey}"
    
    try:
        print("Sending request to map")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print("Map sent response.")
        # Parse the JSON response
        places = response.json()
        count = 1
        places_detail = []
        print("Getting each place's relevant details.")

        for place in places["results"]:
            if place.get("user_ratings_total", 0) < 250:
                 continue
            # place_detail = {
            #     "placeNo": count,
            #     "place_id": place.get("place_id"),
            #     "address": place.get("vicinity"),
            #     "name":place.get("name"),
            #     "ratings": place.get("user_ratings_total", 0),
            #     "types": place.get("types"),
            # }
            place_detail = {
                 'place_no': count,
                 'place_id': place.get('place_id'),
                 'address': place.get('vicinity'),
                 'name': place.get('name'),
                 'latitude': place['geometry']['location']['lat'],
                 'longitude': place['geometry']['location']['lng']
            }
            places_detail.append(place_detail)
            count += 1
        print("Done")
        print(f"Total places after filter: {count}")
        return places_detail
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def get_place(user_data):
    # Extract only required data
    latitude = user_data["latitude"]
    longitude = user_data["longitude"]
    places = get_nearby_places(latitude, longitude)
    if places:
            with open("filtered_places.json", "w", encoding="utf-8") as file:
                json.dump(places, file, indent=3, ensure_ascii=False)
            print("written to a file.")
    else:
        print("No places found or there was an error.")


# Example: balkumari, lalitpur, Nepal
user_data = {
    "latitude": 27.6714861952194,
    "longitude": 85.33868465233498,
    "accuracy": 5,
    "altitude": 1350,
    "timestamp": "2024-02-20T10:45:00Z",
    "provider": "gps"
}


def get_place_details(place_id):
    details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_address,adr_address,name,address_components&key={mapKey}"

    try:
        print("Sending request for details.")
        response = requests.get(details_url, timeout=15)
        response.raise_for_status()
        print("Got details of place.")

        details = response.json()
        full_address = details.get("result", {}).get("formatted_address", "Address Not Found")
        components = details.get("result", {}).get("address_components", [])

        
        print(f"The full address is: {full_address}")
        print(f"Address components: {json.dumps(components, indent=3)}")

    except Exception as e:
        print(f"ERROR OCCURRED: {e}")

get_place_details("ChIJsciVgCoJ6zkRsjUON7SWYKw")




'''
def reverse_geocode(lat, lng):
    geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&language=en&key={mapKey}"
    
    try:
        print("Sending reverse geocode request...")
        response = requests.get(geo_url, timeout=15)
        response.raise_for_status()
        data = response.json()

        if data.get("results"):
            print("FULL ADDRESS: ")
            print(data["results"][0]["formatted_address"]) # Return the best match
        return "Address Not Found"

    except Exception as e:
        print(f"ERROR: {e}")
        return "Address Not Found"
'''