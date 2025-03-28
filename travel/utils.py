from .models import Place
import json
import asyncio

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
        lat = place['latitude']
        lng = place['longitude']
        place_summary = place['summary']
        mainstream = place['mainstream']
        Place.objects.create(name=name, place_id=place_id, full_address=full_address, coordinates={'lng':lng,'lat':lat}, summary=place_summary, mainstream=mainstream)
        print(f"Done for place: {index}")



def get_summary(place_id):
    place = Place.objects.get(place_id=place_id)
    if place:
        return place.summary
    else:
        return None


'''
extract details and save that place to db.
'''
def save_new_place(new_place):
    pid = new_place['place_id']
    pname = new_place['name']
    pfaddress = new_place['full_address']
    pcoordinates = new_place['coordinates']
    psummary = new_place['summary']
    pmainstream = new_place['mainstream']
    Place.objects.create(place_id=pid, name=pname, full_address=pfaddress, coordinates=pcoordinates, summary=psummary, mainstream=pmainstream)
    pass



'''
- send async ai request with semaphore to find summary of given place.
- after getting ai response: 
        - extract 'mainstream'.
        - save to db.        
    along with given details of place, save place to db asynchronously.
return the place summary
'''
async def find_summary(semaphore, pid, pname, pfaddress, pcoordinates):
    pass



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
    SEMAPHORE_LIMIT = 4
    semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)

    tasks = []
    total_summaries = []
    db_summaries = []
    i_summaries = []
    new_places = []

    for place in places:
        pid = place['place_id']
        db_summary = get_summary(pid)
        if db_summary:
            db_summaries.append(db_summary)
        else:
            pname = place['name']
            pfaddress = place['full_address']
            pcoordinates = {'lng':place['lng'], 'lat':place['lat']}
            new_place = {
                'place_id':pid,
                'name':pname,
                'full_address':pfaddress,
                'coordinates':pcoordinates
            }
            new_places.append(new_place)
            task = find_summary(semaphore, pid, pname, pfaddress, pcoordinates)
            tasks.append(task)
    i_summaries = await asyncio.gather(*tasks)

    tasks.clear()
    for index,new_place in enumerate(new_places):
        new_place["summary"] = i_summaries[index]["summary"]
        new_place["mainstream"] = i_summaries[index]["mainstream"]
        task = save_new_place(new_place)
        task.append(tasks)
    await asyncio.gather(*tasks)
    total_summaries = db_summaries + i_summaries
    return total_summaries
