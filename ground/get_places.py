import requests
from key import mapKey
import json
import time
import asyncio
import aiohttp



async def get_place_address(session, place_id):
    address_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_address,adr_address,name,address_components&key={mapKey}"
    try:
        print("Sending request for address.")
        async with session.get(address_url, timeout=15) as response:
            response.raise_for_status()
            print("Got address of place.")
            data = await response.json()
            full_address = data.get("result", {}).get("formatted_address", "Address Not Found")
            return full_address
#        components = data.get("result", {}).get("address_components", [])
#        print(f"The full address is: {full_address}")
#        print(f"Address components: {json.dumps(components, indent=3)}")
    except Exception as e:
        print(f"ERROR OCCURRED: {e}")
        return None


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
        filtered_places_detail = asyncio.run(filter_places(places["results"]))
        return filtered_places_detail
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None



async def filter_places(place_list):
    try:
        count = 1
        places_detail = []
        places_id = []
        tasks = []
        print("Getting each place's relevant details.")
        async with aiohttp.ClientSession() as session:
            for place in place_list:
                if place.get("user_ratings_total", 0) < 250:
                     continue
                place_id = place.get('place_id')
                task = get_place_address(session, place_id)
                tasks.append(task)
                place_detail = {
                     'place_no': count,
                     'place_id': place_id,
                     'name': place.get('name'),
                     'latitude': place['geometry']['location']['lat'],
                     'longitude': place['geometry']['location']['lng']
                }
                places_detail.append(place_detail)
                count += 1
            print("Collecting full address of each place..")
            full_addresses = await asyncio.gather(*tasks)

        for index,address in enumerate(full_addresses):
            if address:
                places_detail[index]['address'] = address
        print("Done")
        print(f"Total places after filter: {count}")
        return places_detail    
    except Exception as e:
        print(f"ERROR OCCURED: {e}")
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



get_place(user_data)

















'''
def reverse_geocode():
    lat = 27.7188945
    lng = 85.31946839999999
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

reverse_geocode()'
'''