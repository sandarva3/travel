from .models import Place
import json

#with open("ground/filtered_places.json", "r", encoding="utf-8") as file:
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
        mainstream = place['mainstream']
        Place.objects.create(name=name, place_id=place_id, full_address=address, coordinates={'lng':lng,'lat':lat}, summary=place_summary, mainstream=mainstream)
        print(f"Done for place: {index}")

def get_summary(place_id):
    place = Place.objects.get(place_id=place_id)
    if place:
        return place.summary
    else:
        return "Place doesn't exist. Need to perform AI search for summary"