from .models import Place
from ground.filtered_places import filtered_places
from django.contrib.gis.geos import Point


'''
print writings filetered places.
loop through each place in places.
extract the required things from each place and assign them to variable.
create a Place instance from those variables.
display done.
'''

def write_filtered_places(filtered_places):
    print("writing filtered places.")
    count = 1
    for place in filtered_places:
        name = place['name']
        address = place['address']
        lat = place['latitude']
        lng = place['lng']
        place_id = place['place_id']

        Place.objects.create(name=name, full_address=address, location=Point(lat,lng), )