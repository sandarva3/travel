
import asyncio
from gemini1 import send_to_gemini
from description import places_list

SEMAPHORE_LIMIT = 5


async def fetch_place_summary(semaphore, place):
    """Fetch summary for a place while controlling concurrency."""
    async with semaphore:
        prompt = f"""Generate a 150-word summary about the place(in a single paragraph) {place}, covering its location, historical or cultural significance, key attractions, 
and any unique features. Then, determine if the place is a mainstream tourist destination. A mainstream tourist destination is defined as a place that is well-known, 
frequently visited by national/international tourists, commonly featured in travel guides, and ranked among top destinations of that country on travel websites. 
If the place regularly attracts many visitors and is a staple in popular travel itineraries, it is mainstream (true). If it is lesser-known, niche, or 
primarily visited by locals or enthusiasts, it is non-mainstream (false).

Provide output in this format:
  place: Place Name,
  summary: <150-word summary>,
  mainstream: true/false
"""
        print(f"Getting summary for: {place}")
        return await asyncio.to_thread(send_to_gemini, prompt)


async def get_details(places):
    """Fetch details of all places with controlled concurrency."""
    semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)
    tasks = [fetch_place_summary(semaphore, place) for place in places]
    summaries = await asyncio.gather(*tasks)
    print("DONE for all places.")
    return summaries


def run_get_details():
    """Run async function inside synchronous execution"""
    print("Running...")
    try:
        places_summaries = asyncio.run(get_details(places_list))
        print("Got places summaries.")

        if input("Print places summaries? (y for yes): ").strip().lower() == "y":
            for count, summary in enumerate(places_summaries, 1):
                print(f"Place {count} summary:\n{summary}")
        else:
            print("BYE")
    except Exception as e:
        print(f"Got error: {e}")


run_get_details()