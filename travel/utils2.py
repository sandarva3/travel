from .models import Place
import json
import asyncio
from ground.get_summary import fetch_place_summary
from travel.utils1 import get_nearby_filtered_places





'''
purpose: find the summary of given place from dB.
'''
def get_summary(place_id, pname):
    try:
        place = Place.objects.get(place_id=place_id)
        if place:
            print(f"Summary for place {pname} exists in DB. ID: {place_id}")
            return place.summary
        else:
            return None
    except:
        pass





'''
purpose: save the given details about places into db.
'''
def save_new_place(pid, pname, pfaddress, pcoordinates, psummary, pmainstream):
    try:
        Place.objects.create(place_id=pid, name=pname, full_address=pfaddress, coordinates=pcoordinates, summary=psummary, mainstream=pmainstream)
        print(f"new place saved. name: {pname}, place_id: {pid}")
    except Exception as e:
        print(f"In travel/utils.save_new_place() ERROR OCCURED: {e}")





'''
- send async ai request with semaphore to find summary of given place.
- after getting ai response: 
        - extract 'mainstream'.
        - save to db.        
    along with given details of place, save place to db asynchronously.
return the place summary
'''
async def find_summary(semaphore, pid, pname, pfaddress, pcoordinates):
    print(f"Getting summary for place: {pname}. PID: {pid}")
    try:
        psummary = await fetch_place_summary(semaphore, pname, pfaddress)
        print("Got summary from ai.")
        mainstream_line = psummary.split("\n")[0]
        if "true" in mainstream_line:
            pmainstream = True
        else:
            pmainstream = False
        await asyncio.to_thread(save_new_place, pid, pname, pfaddress, pcoordinates, psummary, pmainstream)
        return psummary
    except Exception as e:
        print(f"In travel/utils.find_summary() ERROR OCCURED: {e}")





'''
purpose: get summaries of each places in list.
'''
async def get_summaries(places):
    SEMAPHORE_LIMIT = 3
    semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)

    tasks = []
    total_summaries = []
    db_summaries = []
    i_summaries = []

    try:
        for index,place in enumerate(places):
            pid = place['place_id']
            pname = place['name']
            db_summary = await asyncio.to_thread(get_summary, pid, pname)
            if db_summary:
                print("Place is found in db.")
                db_summaries.append(db_summary)
            else:
                print(f"Place({pid}) not found in db. Sending ai request..")
                pfaddress = place['full_address']
                pcoordinates = {'lng':place['lng'], 'lat':place['lat']}
                print(f"find_summary for place {index}")
                task = find_summary(semaphore, pid, pname, pfaddress, pcoordinates)
                tasks.append(task)
        i_summaries = await asyncio.gather(*tasks)
        total_summaries = db_summaries + i_summaries
        return total_summaries
    except Exception as e:
        print(f"In travel/utils.get_summaries() ERROR OCCURED: {e}")





def run_get_summaries(filtered_places):
    try:
        sums = asyncio.run(get_summaries(filtered_places))
        if sums:
            print("Cool summaries is found.")
            print("\n".join(f"- {s}\n\n\n\n\n" for s in sums))
            print(f"Length of sums: {len(sums)}")
        else:
            print("In travel/utils.run_get_summaries() NO ERROR OCCURED but 'sums' returned None")
    except Exception as e:
        print(f"In travel/utils.run_get_summaries() ERROR OCCURED: {e}")