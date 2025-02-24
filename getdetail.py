import requests
import json
from key import mapKey

def get_place_details(place_id):
    """
    Fetches detailed information about a place using the Google Places API
    and saves it into a JSON file.
    """
#    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,rating,user_ratings_total,formatted_address,geometry,types,website,international_phone_number,reviews,opening_hours&key={mapKey}"
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={mapKey}"
   
    try:
        print(f"Sending request for place_id: {place_id}")
        response = requests.get(url, timeout=(5, 10))  # Timeout for reliability
        print("Got response")
        response.raise_for_status()  # Raise an error if response is not 2xx
        
        place_data = response.json()

        if place_data.get("status") != "OK":
            print(f"Error fetching place details: {place_data.get('status')}")
            return None
        return place_data
    except Exception as e:
        print(f"Exception occured: {e}")
        return None
'''
        # Extract relevant details
        result = place_data.get("result", {})

        place_detail = {
            "place_id": place_id,
            "name": result.get("name"),
            "address": result.get("formatted_address"),
            "ratings": result.get("rating"),
            "total_ratings": result.get("user_ratings_total"),
            "types": result.get("types"),
            "website": result.get("website"),
            "phone_number": result.get("international_phone_number"),
            "location": result.get("geometry", {}).get("location"),
            "opening_hours": result.get("opening_hours", {}).get("weekday_text"),
            "reviews": result.get("reviews")  # Contains user reviews if available
        }

        # Save to JSON file
        with open("place_detail.json", "w", encoding="utf-8") as json_file:
            json.dump(place_detail, json_file, indent=4, ensure_ascii=False)

        print(f"Place details saved to place_detail.json")
        return place_detail
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
'''

place_id = "ChIJrciCm40Y6zkR93t5EOS9Ma4"
place_detail = get_place_details(place_id)
with open("place_details.json", "w", encoding="utf-8") as file:
    json.dump(place_detail, file, indent=3, ensure_ascii=False)
print("written to a file.")