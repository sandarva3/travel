
import asyncio
from gemini1 import send_to_gemini
from filtered_places import filtered_places
import json

SEMAPHORE_LIMIT = 3


async def fetch_place_summary(semaphore, place_name, place_address):
    """Fetch summary for a place while controlling concurrency."""
    async with semaphore:
        prompt = f"""Generate a 150-word summary about the place(in a single paragraph): {place_name}, {place_address}, covering its location, historical or cultural significance, key attractions, 
and any unique features. Then, determine if the place is a mainstream tourist destination. A mainstream tourist destination is defined as a place that is well-known, 
frequently visited by national/international tourists, commonly featured in travel guides, and ranked among top destinations of that country on travel websites. 
If the place regularly attracts many visitors and is a staple in popular travel itineraries, it is mainstream (true). If it is lesser-known, niche, or 
primarily visited by locals or enthusiasts, it is non-mainstream (false).

Provide output 'exactly' in this format:
  <150-word summary>.

  mainstream: true/false
"""
        print(f"Getting summary for: {place_name}")
        return await asyncio.to_thread(send_to_gemini, prompt)


async def get_details(places):
    """Fetch details of all places with controlled concurrency."""
    semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)
    tasks = [fetch_place_summary(semaphore, place['name'], place['address']) for place in places]
#    count = 0
    # tasks = []
    # for place in places:
    #     count += 1
    #     task = fetch_place_summary(semaphore, place)
    #     tasks.append(task)
    #     if count == 5:
    #         asyncio.sleep(2)
    #     elif count == 10:
    #         asyncio.sleep(2)
    #     elif count == 15:
    #         asyncio.sleep(2)
    #     elif count == 20:
    #         asyncio.sleep(20)
    summaries = await asyncio.gather(*tasks)
    print("DONE for all places.")
    return summaries


def save_summary(places_summaries):
    full_summary_list = []
    for index,filtered_place in enumerate(filtered_places):
        place_summary = places_summaries[index]
        filtered_place["summary"] = place_summary
    print("attached summary to each places")
    with open("filtered_places.json", "w") as file:
        json.dump(filtered_places, file, indent=3, ensure_ascii=False)
    print("saved the the filtered_places file alogn with summary.")


def run_get_details():
    """Run async function inside synchronous execution"""
    print("Running...")
    try:
        places_summaries = asyncio.run(get_details(filtered_places))
        print("Got places summaries.")
        if input("Print places summaries? (y for yes): ").strip().lower() == "y":
            for count, summary in enumerate(places_summaries, 1):
                print(f"Place {count} summary:\n{summary}")
        else:
            print("BYE")
        save_summary(places_summaries)
    except Exception as e:
        print(f"Got error: {e}")


run_get_details()