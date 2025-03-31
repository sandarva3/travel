from ground2.dummy_user import user_preferences
from .models import Place
import requests
import json
from ground2.get_personalized_places import ask_gemini_places_recommendation





def get_ai_response_for_places_recommendation(user_details, places_list):
    prompt = f"""
You have two things: User_details, and Places_list. Analyze and understand both of them. From there only return a id of place/s which user might prefer.
EXTREMELY IMPORTANT: Return place_id only with comma for each.

User_details: {user_details}


Places_list: {places_list}
"""
    try:
        print("Asking gemini...")
        response = ask_gemini_places_recommendation(prompt).strip()
        print("Gemini sent response.")
        return response
    except Exception as e:
        print(f"In ground2/get_saved_places.get_ai_response() ERROR OCCURED: {e}")





def get_all_saved_places():
    all_places_list = []
    all_places = Place.objects.all()
    for index,place in enumerate(all_places, start=1):
        place_dict= {}
#        place_dict["place_no"] = index
#        place_dict["place_name"] = place.name
        place_dict["place_id"] = place.place_id
        place_dict["summary"] = place.summary
        all_places_list.append(place_dict)
        if index == 50:
            break
    return all_places_list





def main_fn_for_places_recommendation():
    try:
        count = 0
        saved_places_list = get_all_saved_places()
        saved_places_list_length = len(saved_places_list)
        saved_places_list2 = [saved_places_list[i:i+10] for i in range(0, saved_places_list_length, 10)]
        for i in saved_places_list2:
            count += 1
        print(f"Total sublists: {count}")
        user_preferences_json = json.dumps(user_preferences, indent=3)
        saved_places_list2_json = json.dumps(saved_places_list2[0], indent=3)
        ai_recommendations = get_ai_response_for_places_recommendation(user_preferences_json, saved_places_list2_json)
        print("AI recommendation")
        print(ai_recommendations)
        print(f"Raw AI Response: {repr(ai_recommendations)}")  # Shows hidden chars
        print(type(ai_recommendations))
        try:
            dict1 = json.loads(ai_recommendations)
            print("Successfully parsed AI response!")
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
        return "COOL"
    except Exception as e:
        print(f"In ground2/get_saved_places.main_fn_for_places_recommendation() ERROR OCCURED: {e}")
