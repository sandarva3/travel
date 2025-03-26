import requests
from key import mapKey
import json


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
        full_address2 = ""
        for component in components:
            name= component["long_name"]
            full_address2 = f"{full_address2}, {name}"
        
        print(f"The full address is: {full_address}")
        print(f"Address components: {json.dumps(components, indent=3)}")
        print(f"Full address 2 is: {full_address2}")
    except Exception as e:
        print(f"ERROR OCCURRED: {e}")

get_place_details("ChIJrciCm40Y6zkR93t5EOS9Ma4")