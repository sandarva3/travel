import requests
from key import mapKey
import json
import time
from typing import List, Dict, Optional

def get_place_details(place_id: str) -> Optional[Dict]:
    """
    Fetch detailed place information using Google Maps Place Details API.
    
    Args:
        place_id (str): The Google Places ID
        
    Returns:
        Optional[Dict]: Detailed place information or None if request fails
    """
    fields = "name,editorial_summary,formatted_address,types,user_ratings_total,rating,reviews,photos,opening_hours,website"
    details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={mapKey}"
    
    try:
        response = requests.get(details_url, timeout=7)
        response.raise_for_status()
        details_data = response.json()
        
        if details_data.get("status") != "OK":
            print(f"Details API returned non-OK status for {place_id}: {details_data.get('status')}")
            return None
            
        return details_data.get("result")
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch details for {place_id}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON for {place_id}: {e}")
        return None

def get_nearby_places(latitude: float, longitude: float, min_ratings: int = 200, max_results: int = 60) -> Optional[List[Dict]]:
    """
    Fetch nearby tourist attractions using Google Places API with pagination support
    and detailed information for each place.
    
    Args:
        latitude (float): Location latitude
        longitude (float): Location longitude
        min_ratings (int): Minimum number of ratings required to include a place
        max_results (int): Maximum number of results to return
        
    Returns:
        Optional[List[Dict]]: List of filtered place details or None if request fails
    """
    radius = 50000  # maximum allowed radius in meters
    place_type = "tourist_attraction"
    filtered_places = []
    next_page_token = None
    total_processed = 0
    
    while True:
        # Construct URL with or without page token
        base_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&type={place_type}&key={mapKey}"
        url = f"{base_url}&pagetoken={next_page_token}" if next_page_token else base_url
        
        try:
            print(f"Fetching tourist attractions... (Filtered places so far: {len(filtered_places)})")
            response = requests.get(url, timeout=7)
            response.raise_for_status()
            
            places_data = response.json()
            
            if places_data.get("status") != "OK":
                print(f"API returned non-OK status: {places_data.get('status')}")
                break
            
            # Process places from this page
            for place in places_data["results"]:
                total_processed += 1
                
                # Initial rating check to avoid unnecessary detail requests
                if place.get("user_ratings_total", 0) < min_ratings:
                    continue
                
                # Get detailed information
                place_id = place.get("place_id")
                details = get_place_details(place_id)
                
                if details:
                    place_info = {
                        "placeNo": len(filtered_places) + 1,
                        "name": details.get("name"),
                        "place_id": place_id,
                        "address": details.get("formatted_address"),
                        "description": details.get("editorial_summary", {}).get("overview", "No description available"),
                        "ratings": {
                            "rating": details.get("rating", 0),
                            "total_ratings": details.get("user_ratings_total", 0)
                        },
                        "types": details.get("types", []),
                        "location": {
                            "lat": place.get("geometry", {}).get("location", {}).get("lat"),
                            "lng": place.get("geometry", {}).get("location", {}).get("lng")
                        },
                        "website": details.get("website", "Not available"),
                        "opening_hours": details.get("opening_hours", {}).get("weekday_text", [])
                    }
                    filtered_places.append(place_info)
                    
                    # Check if we've reached the maximum requested results
                    if len(filtered_places) >= max_results:
                        print(f"Reached maximum requested results: {max_results}")
                        return filtered_places
            
            # Check for next page token
            next_page_token = places_data.get("next_page_token")
            if not next_page_token:
                print("No more pages available")
                break
                
            # Important: Wait before making the next request
            print("Waiting for next page token to become valid...")
            time.sleep(2)
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            break
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
    
    print(f"Total places processed: {total_processed}")
    print(f"Places meeting criteria: {len(filtered_places)}")
    return filtered_places if filtered_places else None

def main():
    # Example Usage: Balkumari, Lalitpur, Nepal
    user_data = {
        "latitude": 27.6714861952194,
        "longitude": 85.33868465233498,
        "accuracy": 5,
        "altitude": 1350,
        "timestamp": "2024-02-20T10:45:00Z",
        "provider": "gps"
    }
    
    places = get_nearby_places(
        latitude=user_data["latitude"],
        longitude=user_data["longitude"],
        min_ratings=200,  # Minimum ratings threshold
        max_results=60    # Maximum places to return
    )
    
    if places:
        try:
            with open("output.json", "w", encoding="utf-8") as file:
                json.dump(places, file, indent=4, ensure_ascii=False)
            print("Data successfully written to output.json")
        except IOError as e:
            print(f"Failed to write to file: {e}")
    else:
        print("No places found or there was an error.")

if __name__ == "__main__":
    main()