#send list of places to an ai and get response asynchronously.
from gemini1 import send_to_gemini
import asyncio
#from description import places_list


async def get_details(places):
    prompt = lambda place: f"""Search about this place and tell 150 words summary about it, in single paragraph.. Place = {place} 
EXTREMELY IMPORTANT: ONLY TELL SUMMARY(WITH PLACE NAME AS TITLE), NOTHING ELSE, and also tell if it's 'mainstream' tourist spot or not, like 'mainstream':true/false. 
MORE EXTREMELY IMPORTANT: check mainstream thing carefully."""
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
        places_summaries = asyncio.run(get_details(places=places))
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