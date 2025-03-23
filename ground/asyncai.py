#send list of places to an ai and get response asynchronously.
from gemini1 import send_to_gemini
import asyncio


async def get_details(places):
    prompt = lambda place: f"""Search about this place and tell around 150 words summary about it. Place = {place} 
EXTREMELY IMPORTANT: ONLY TELL SUMMARY, NOTHING ELSE."""
    count = 1
    summaries = []
    for place in places:
#        summary = await asyncio.to_thread(send_to_gemini, prompt(place)) #this way function waits at each iteration, making it sequential.
        task = asyncio.to_thread(send_to_gemini, prompt(place)) #here we create coroutines, which executes parallely
        print(f"getting place {count} summary.")
        count += 1
        summaries.append(task) # here we append coroutines to list.
    
    await asyncio.gather(*summaries)  # we wait until all coroutines resolves. and gather() expects coroutines, any other datatype will cause it to fail.
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
        "name": "Kailashnath Mahadev Statue",
        "address": "Sanga, सुर्यविनायक 44800, Nepal"
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
        inp = input("Print places summaries?: y for yes")
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