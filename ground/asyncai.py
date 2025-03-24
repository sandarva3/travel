#send list of places to an ai and get response asynchronously.
from gemini1 import send_to_gemini
import asyncio
from description import places_list


async def get_details(places):
    prompt = lambda place: f"""Generate a 150-word summary about the place {place}, covering its location, historical or cultural significance, key attractions, 
and any unique features. Then, determine if the place is a mainstream tourist destination. A mainstream tourist destination is defined as a place that is well-known, 
frequently visited by national/international tourists, commonly featured in travel guides, and ranked among top destinations of the that country on travel websites. 
If the place regularly attracts many visitors and is a staple in popular travel itineraries, it is mainstream (true). If it is lesser-known, niche, or 
primarily visited by locals or enthusiasts, it is non-mainstream (false).

Provide output in this format:
{{
  place: Place Name,
  summary: <150-word summary>,
  mainstream: true/false
}}

"""
    count = 1
    tasks = []
    for place in places:
#        summary = await asyncio.to_thread(send_to_gemini, prompt(place)) #this way function waits at each iteration, making it sequential.
        task = asyncio.to_thread(send_to_gemini, prompt(place)) #here we create coroutines, which executes parallely
        print(f"getting place {count} summary.")
        count += 1
        tasks.append(task) # here we append coroutines to list.
    
    summaries = await asyncio.gather(*tasks)  # we wait until all coroutines resolves. and gather() expects coroutines, any other datatype will cause it to fail.
    print("DONE for all places.")
    return summaries


def run_get_details():
    print("Running...")
    places = [{
        "name": "Hotel Shanker - Palatial Heritage Kathmandu",
        "address": "Lazimpat, Kathmandu 44600, Nepal"
    },
    {
        "name": "Kopan Monastery",
        "address": "P9V7+3X7 Ward 11, Budhanilkantha 44600, Nepal"
    },
    {
        "name": "Pasupatinath Temple",
        "address": "Chabahil, Nepal"
    },
    {
        "name": "Handigaun",
        "address": "Handigaun Marg, Kathmandu 44600, Nepal"
    },
    {
        "name": "Swoyambhu Mahachaitya",
        "address": "P77R+X52, BHAGANPAU 44600, Nepal"
    }]
    try:
        places_summaries = asyncio.run(get_details(places=places_list))
        print("Got places Summaries")
        inp = input("Print places summaries?: y for yes: ")
        if inp=="y":
            count = 1
            for place_summary in places_summaries:
                print(f"place {count} summary:")
                print(place_summary)
                count += 1
        else:
            print("BYE")
    except Exception as e:
        print(f"Got error: {e}")



run_get_details()