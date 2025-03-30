import requests
import json
from get_personalized_places import ask_gemini
from dummy_user import user_preferences






def get_ai_response(user_details, places_list):
    prompt = f"""
You have two things: User_details, and Places_list. Analyze and understand both of them. From ther 'only' return a place/s which user might prefer.
Return place_id only. Provide your response in full json.

User details: {user_details}


places_list: {places_list}
"""
    try:
        print("Asking gemini...")
        response = ask_gemini(prompt)
        print("Gemini sent response.")
        return response
    except Exception as e:
        print(f"In ground2/get_saved_places.get_ai_response() ERROR OCCURED: {e}")



def start():
    first_ten_places = []
    second_ten_places = []
    third_ten_places = []
    fourth_ten_places = []
    fifth_ten_places = []
    full_places_list = []
    saved_places = requests.get("http://127.0.0.1:8000/allPlaces")
    for index,place in enumerate(saved_places.json()):
        if 0 <= index < 10:
            first_ten_places.append(place)
        elif 10 <= index < 20:
            second_ten_places.append(place)
        elif 20 <= index < 30:
            third_ten_places.append(place)
        elif 30 <= index < 40:
            fourth_ten_places.append(place)
        elif 40 <= index < 50:
            fifth_ten_places.append(place)
    full_places_list = first_ten_places + second_ten_places + third_ten_places + fourth_ten_places + fifth_ten_places

    ai_response = get_ai_response(user_preferences, json.dumps(first_ten_places, indent=3))
    print(ai_response)



start()