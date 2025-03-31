from ground2.dummy_user import user_preferences1
from .models import Place
import requests
import json
from ground2.get_personalized_places import ask_gemini_places_recommendation
import asyncio

user_preferences = user_preferences1





def get_pname_from_db(pid):
    try:
        return Place.objects.get(place_id=pid).name
    except Exception as e:
        print(f"In travel/utils2.get_pname_from_db(), for pid: {pid} .  ERROR OCCURED: {e}")
        return None





async def process_ai_response(ai_response):
    try:
        ai_recommended_pname_list = []
        ai_recommended_id_list = ai_response.split(',')
        print(f"ai_recommended_places = {ai_recommended_id_list}")
        for pid in ai_recommended_id_list:
            pid = pid.strip()
            if pid and pid != "":
                pname = await asyncio.to_thread(get_pname_from_db, pid)
                ai_recommended_pname_list.append(pname)
            else:
                print("In travel/utils2.process_ai_response() NO ERROR but wrong pid by AI.")
        print("The best places for this user are: ")
        for name in ai_recommended_pname_list:
            print(f"- {name}")
        return ai_recommended_pname_list
    except Exception as e:
        print(f"In travel/utils2.process_ai_response() ERROR OCCURED: {e}")





def get_ai_response_for_places_recommendation(user_details, places_list):
    prompt = f"""
You have two things: User_details, and Places_list. Analyze and understand both of them. From there only return a id of place/s which user most likely might prefer, be concise on this.
EXTREMELY IMPORTANT: Return place_id only with comma separating each of them. 
EXTREMELY IMPORTANT: if None of the places matches then return only 2 spaces, no other characters.


User_details: {user_details}


Places_list: {places_list}
"""
    try:
        print("Asking gemini...")
        response = ask_gemini_places_recommendation(prompt).strip()
        print("Gemini sent response.")
        return response
    except Exception as e:
        print(f"In travel/utils2.get_ai_response_for_places_recommendation() ERROR OCCURED: {e}")





def get_all_saved_places():
    try: 
        all_places_list = []
        all_places = Place.objects.all()
        for index,place in enumerate(all_places, start=1):
            place_dict= {}
            place_dict["place_id"] = place.place_id
            place_dict["summary"] = place.summary
            all_places_list.append(place_dict)
        return all_places_list
    except Exception as e:
        print(f"In travel/utils2.get_all_saved_places() ERROR OCCURED: {e}")





async def get_places_recommendation():
    try:
        tasks = []
        best_pnames = []
        saved_places_list = await asyncio.to_thread(get_all_saved_places)
        saved_places_list_length = len(saved_places_list)
        saved_places_sublists = [saved_places_list[i:i+10] for i in range(0, saved_places_list_length, 10)]

        user_preferences_json = json.dumps(user_preferences, indent=3)

        for index,sublist in enumerate(saved_places_sublists):
            print(f"Getting ai response for sublist {index}")
            sublist_json = json.dumps(sublist, indent=3)
            task = asyncio.to_thread(get_ai_response_for_places_recommendation, user_preferences_json, sublist_json)
            tasks.append(task)
        ai_recommendations = await asyncio.gather(*tasks)
        print("Gathered ai_recommendations.")

        tasks.clear()
        for index,recommendation in enumerate(ai_recommendations):
            print(f"Processing ai response of sublist {index}")
            task = process_ai_response(recommendation)
            tasks.append(task)
        best_pnames = await asyncio.gather(*tasks)
        print("Gathered best_pnames.")
        print("best_pnames:")
        print(best_pnames)
        return best_pnames
    except Exception as e:
        print(f"In ground2/get_saved_places.get_places_recommendation() ERROR OCCURED: {e}")





def run_get_places_recommendation():
    try:
        best_pnames = asyncio.run(get_places_recommendation())
        return best_pnames
    except Exception as e:
        print(f"In travel/utils2.run_get_places_recommendation() ERROR OCCURED: {e}")