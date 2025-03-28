from .models import Place
import json
import asyncio
from ground.get_summary import fetch_place_summary
#with open("ground/filtered_places.json", "r", encoding="utf-8") as file:
#    filtered_places = json.load(file)
#    print("Converted json file to dict object.")



'''
-purpose: to enter all filtered places into db
print writings filetered places.
loop through each place in places.
extract the required things from each place and assign them to variable.
create a Place instance from those variables.
display done.
'''
def write_filtered_places(filtered_places):
    print("writing filtered places.")
    for index,place in enumerate(filtered_places):
        name = place['name']
        place_id = place['place_id']
        full_address = place['full_address']
        lat = place['lat']
        lng = place['lng']
        place_summary = place['summary']
        mainstream = place['mainstream']
        Place.objects.create(name=name, place_id=place_id, full_address=full_address, coordinates={'lng':lng,'lat':lat}, summary=place_summary, mainstream=mainstream)
        print(f"Done for place: {index}")



def get_summary(place_id, pname):
    try:
        place = Place.objects.get(place_id=place_id)
        if place:
            print(f"Summary for place {pname} exists in DB. ID: {place_id}")
            return place.summary
        else:
            return None
    except Exception as e:
        print(f"ERROR OCCURED in get_summary()")


'''
extract details and save that place to db.
'''
def save_new_place(pid, pname, pfaddress, pcoordinates, psummary, pmainstream):
    try:
        Place.objects.create(place_id=pid, name=pname, full_address=pfaddress, coordinates=pcoordinates, summary=psummary, mainstream=pmainstream)
        print(f"new place saved. name: {pname}, place_id: {pid}")
    except Exception as e:
        print(f"ERROR OCCURED: {e}")



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
        print("Got summary.")
        mainstream_line = psummary.split("\n")[0]
        if "true" in mainstream_line:
            pmainstream = True
        else:
            pmainstream = False
        await asyncio.to_thread(save_new_place, pid, pname, pfaddress, pcoordinates, psummary, pmainstream)
        return psummary
    except Exception as e:
        print(f"ERROR OCCURED: {e}")



'''
purpose: get summaries of each places in list.
...
wait until all tasks are resolved and i_summaries have summary for new places.
after getting summary for new places, save that into db.(do this async if you can)
    to save it into db: extract place required details.
    instead of doing everything here, create another async function to save into db.
then combine db_summaries and i_summaries, let it be called a total_summaries list
then return that total_summaries list, which contains summary of every place in a list.
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
                print("Place is not found in db.")
                pfaddress = place['full_address']
                pcoordinates = {'lng':place['lng'], 'lat':place['lat']}
                print(f"find_summary for place {index}")
                task = find_summary(semaphore, pid, pname, pfaddress, pcoordinates)
                tasks.append(task)
        i_summaries = await asyncio.gather(*tasks)
        total_summaries = db_summaries + i_summaries
        return total_summaries
    except Exception as e:
        print(f"ERROR OCCURED: {e}")


def run_get_summaries():
    with open("ground/filtered_places1.json", "r", encoding="utf-8") as file:
        filtered_places = json.load(file)
    print("Converted json file to dict object.")
    sums = asyncio.run(get_summaries(filtered_places))
    if sums:
        print("Cool summaries is found.")
        print("\n".join(f"  - {s}\n\n\n\n\n" for s in sums))
        print(f"Length of sums: {len(sums)}")
    else:
        print("error occured while finding sums")