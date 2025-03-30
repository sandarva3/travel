from ground2.dummy_user import user_preferences
from .models import Place


def get_all_places():
    all_places_dict = []
    all_places = Place.objects.all()
    for index,place in enumerate(all_places, start=1):
        place_dict= {}
        place_dict["place_name"] = place.name
        place_dict["place_id"] = place.place_id
        place_dict["summary"] = place.summary
        all_places_dict.append(place_dict)
        if index == 50:
            break
    return all_places_dict