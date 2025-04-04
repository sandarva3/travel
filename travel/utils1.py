import requests
from ground.key import mapKey
import json
import time
import asyncio
import aiohttp





async def get_place_address(session, place_id):
    address_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_address,name&language=en&key={mapKey}"
    try:
        print("Sending request for full address.")
        async with session.get(address_url, timeout=15) as response:
            response.raise_for_status()
            print("Got full address of place.")
            data = await response.json()
            full_address = data.get("result", {}).get("formatted_address", "Address Not Found")
            return full_address
#        components = data.get("result", {}).get("address_components", [])
#        print(f"The full address is: {full_address}")
#        print(f"Address components: {json.dumps(components, indent=3)}")
    except Exception as e:
        print(f"ERROR OCCURRED: {e}")
        return None





'''
Google map sends total 60 places details in response. But in a single page only 20 places are found.
So, for other places we need to go to next page through next_page_token.
'''
def get_nearby_places(latitude, longitude):
    radius = 50000
    all_places = []
    place_type = "tourist_attraction"
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&type={place_type}&language=en&key={mapKey}"
    try:
        print("Sending request to map")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print("Map sent response.")
        # Parse the JSON response
        data = response.json()
        all_places.extend(data.get("results", []))

        while "next_page_token" in data:
            next_page_token = data["next_page_token"]
            next_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key={mapKey}"
            time.sleep(2)  # Delay to ensure token is valid
            print("Fetching next page...")
            response = requests.get(next_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            all_places.extend(data.get("results", []))

        filtered_places_detail = asyncio.run(filter_places(all_places))
        return filtered_places_detail
    except requests.exceptions.RequestException as e:
        print(f"ERROR OCCURED IN get_places.get_nearby_places(). Request failed: {e}")
        return None





async def filter_places(place_list):
    try:
        count = 0
        places_detail = []
        places_id = []
        tasks = []
        print("Getting each place's relevant details.")
        async with aiohttp.ClientSession() as session:
            for place in place_list:
                if place.get("user_ratings_total", 0) < 300:
                     continue
                place_id = place.get('place_id')
                task = get_place_address(session, place_id)
                tasks.append(task)
                count += 1
                place_detail = {
                     'place_id': place_id,
                     'name': place.get('name'),
                     'lat': place['geometry']['location']['lat'],
                     'lng': place['geometry']['location']['lng']
                }
                places_detail.append(place_detail)
            print("Collecting full address of each place..")
            full_addresses = await asyncio.gather(*tasks)

        for index,full_address in enumerate(full_addresses):
            places_detail[index]['full_address'] = full_address
        print("Done")
        print(f"Total places after filter: {count}")
        return places_detail    
    except Exception as e:
        print(f"ERROR OCCURED: {e}")
        return None





def get_nearby_filtered_places(longitude, latitude):
    try:
        places = get_nearby_places(latitude, longitude)
        if places:
                return places
        else:
            print("In trave/utils3.get_place() NO ERROR but 'places' returned None.")
    except Exception as e:
        print(f"In trave/utils3.get_place() ERROR OCCURED: {e}")






