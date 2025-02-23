import requests
from key import mapKey
import json
import time
from typing import List, Dict, Optional
from math import radians, sin, cos, sqrt, atan2




def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth using Haversine formula.
    
    Args:
        lat1, lon1: Latitude and longitude of point 1
        lat2, lon2: Latitude and longitude of point 2
        
    Returns:
        Distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers

    # Convert latitude and longitude to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine formula
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    
    return round(distance, 2)




def get_distance_matrix(origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float, api_key: str) -> Optional[Dict]:
    """
    Get distance and duration using Google Distance Matrix API.
    
    Args:
        origin_lat, origin_lon: Starting point coordinates
        dest_lat, dest_lon: Destination coordinates
        api_key: Google Maps API key
        
    Returns:
        Dictionary containing distance and duration information or None if request fails
    """
    url = (
        f"https://maps.googleapis.com/maps/api/distancematrix/json?"
        f"origins={origin_lat},{origin_lon}&"
        f"destinations={dest_lat},{dest_lon}&"
        f"mode=driving&"  # Specify travel mode
        f"language=en&"   # Response language
        f"key={api_key}"
    )
    
    try:
        print(f"Fetching driving distance to {dest_lat},{dest_lon}...")
        response = requests.get(url, timeout=7)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "OK":
            print(f"Distance Matrix API returned status: {data.get('status')}")
            return None
            
        elements = data.get("rows", [{}])[0].get("elements", [{}])[0]
        
        if elements.get("status") != "OK":
            print(f"Distance Matrix element status: {elements.get('status')}")
            return None
            
        return {
            "distance": {
                "text": elements["distance"]["text"],
                "value": elements["distance"]["value"]  # in meters
            },
            "duration": {
                "text": elements["duration"]["text"],
                "value": elements["duration"]["value"]  # in seconds
            }
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Request to Distance Matrix API failed: {e}")
        return None
    except KeyError as e:
        print(f"Unexpected response format: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in distance matrix calculation: {e}")
        return None




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




def get_nearby_places(latitude: float, longitude: float, min_ratings: int = 200, max_results: int = 60, use_distance_matrix: bool = False) -> Optional[List[Dict]]:
    """
    Fetch nearby tourist attractions with distance information.
    
    Args:
        latitude, longitude: Location coordinates
        min_ratings: Minimum number of ratings required
        max_results: Maximum number of results to return
        use_distance_matrix: If True, use Google Distance Matrix API for accurate travel distance
    """
    radius = 50000  # maximum allowed radius in meters
    place_type = "tourist_attraction"
    filtered_places = []
    next_page_token = None
    total_processed = 0
    
    while True:
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
            
            for place in places_data["results"]:
                total_processed += 1
                
                if place.get("user_ratings_total", 0) < min_ratings:
                    continue
                
                place_id = place.get("place_id")
                details = get_place_details(place_id)
                
                if details:
                    # Get place coordinates
                    dest_lat = place["geometry"]["location"]["lat"]
                    dest_lng = place["geometry"]["location"]["lng"]
                    
                    # Calculate straight-line distance
                    straight_line_distance = calculate_haversine_distance(
                        latitude, longitude, dest_lat, dest_lng
                    )
                    
                    # Initialize distance info
                    distance_info = {
                        "straight_line_km": straight_line_distance,
                        "driving": None
                    }
                    
                    # Get driving distance if requested
                    if use_distance_matrix:
                        matrix_result = get_distance_matrix(
                            latitude, longitude, 
                            dest_lat, dest_lng,
                            mapKey
                        )
                        if matrix_result:
                            distance_info["driving"] = matrix_result
                    
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
                            "lat": dest_lat,
                            "lng": dest_lng
                        },
                        "distance": distance_info,
                        "website": details.get("website", "Not available"),
                        "opening_hours": details.get("opening_hours", {}).get("weekday_text", [])
                    }
                    filtered_places.append(place_info)
                    
                    if len(filtered_places) >= max_results:
                        print(f"Reached maximum requested results: {max_results}")
                        return filtered_places
            
            next_page_token = places_data.get("next_page_token")
            if not next_page_token:
                print("No more pages available")
                break
            
            print("Waiting for next page token to become valid...")
            time.sleep(2)
            
        except Exception as e:
            print(f"Error fetching places: {e}")
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
        max_results=60,  # Maximum places to return
        use_distance_matrix=False,
    )
    
    if places:
        # Sort places by straight-line distance
        places.sort(key=lambda x: x["distance"]["straight_line_km"])
        
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