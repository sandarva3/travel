from .models import Place
import json
from django.contrib.gis.geos import Point

#with open("../ground/filtered_places.json", "r", encoding="utf-8") as file:
#    filtered_places = json.load(file)
#    print("Converted json file to dict object.")


'''
-purpose: to enter all filtered places into db
print writings filetered places.
loop through each place in places.
extract the required things from each place and assign them to variable.
create a Place instance from those variables.
display done.
'''

def write_filtered_places(filtered_places):
    print("writing filtered places.")
    for index,place in enumerate(filtered_places):
        name = place['name']
        place_id = place['place_id']
        address = place['address']
        lat = place['latitude']
        lng = place['longitude']
        place_summary = place['summary']
        Place.objects.create(name=name, place_id=place_id, full_address=address, location=Point(lng,lat), summary=place_summary)
        print(f"Done for place: {index}")
