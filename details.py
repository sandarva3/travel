import requests
import time
import json


def search_wikipedia(place_name):
    """Search Wikipedia for the best-matching page title."""
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": place_name,
        "format": "json"
    }
    
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        data = response.json()
        search_results = data.get("query", {}).get("search", [])
        if search_results:
            return search_results[0]["title"]  # Return the best-matching title
    return None

def get_wikipedia_summary(place_name):
    """Fetches the summary (3-5 sentences) from Wikipedia API for a given place name."""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{place_name.replace(' ', '_')}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No description available.")
    else:
        return "No description found on Wikipedia."

places = [
    {"name": "Hotel Shanker - Palatial Heritage Kathmandu", "address": "Lazimpat, Kathmandu 44600, Nepal"},
    {"name": "Kopan Monastery", "address": "P9V7+3X7 Ward 11, Budhanilkantha 44600, Nepal"},
    {"name": "Kailashnath Mahadev Statue", "address": "Sanga, सुर्यविनायक 44800, Nepal"},
    {"name": "Handigaun", "address": "Handigaun Marg, Kathmandu 44600, Nepal"},
    {"name": "Swoyambhu Mahachaitya", "address": "P77R+X52, BHAGANPAU 44600, Nepal"},
    {"name": "Kathmandu Fun Valley", "address": "अरनिको राजमार्ग Bhaktapur, Araniko Highway Bhaktapur, Suryabinayak 44805, Nepal"},
    {"name": "Nepal Art Council", "address": "M8RF+WF2, Madan Bhandari Road, Kathmandu 44600, Nepal"},
    {"name": "Namobuddha Monastery", "address": "HHCM+F2R, Namobuddha Rd, Simalchaur Syampati 45200, Nepal"},
    {"name": "Kathmandu Fun Park", "address": "Pradarshani Marg, Kathmandu 44600, Nepal"},
    {"name": "Hanuman Dhoka", "address": "Hanuman Dhoka Sadak, Kathmandu 44600, Nepal"},
    {"name": "Garden of Dreams", "address": "P877+MR2, Tridevi Sadak, Kathmandu 44600, Nepal"},
    {"name": "Hotel Royal Kathmandu", "address": "Mitranagar 26, Kathmandu 44600, Nepal"},
    {"name": "Pilot Baba Ashram", "address": "JCRF+333, Ghyampe Danda Sadak, Anantalingeshwar, Nepal"},
    {"name": "Patan Darbar Square", "address": "Lalitpur 44600, Nepal"},
    {"name": "Kathmandu Durbar Square", "address": "Kathmandu 44600, Nepal"},
    {"name": "Bhaktapur Durbar Square", "address": "Durbar square, Bhaktapur 44800, Nepal"},
    {"name": "Shivapuri Nagarjun National Park", "address": "44600, Nepal"},
    {"name": "Patan Museum", "address": "M8FG+944, भिन्द्यो क्व - सौग: लँ, Lalitpur 44700, Nepal"},
    {"name": "Ghyampe Danda", "address": "JCRC+FGW, Ghyampe Danda Sadak, Anantalingeshwar 44800, Nepal"},
    {"name": "Shree Kamaladi Ganesh Temple", "address": "P859+4P7, Kamaladi Marg, Kathmandu 44605, Nepal"},
    {"name": "Casino Mahjong", "address": "Soaltee Crown Plaza, Tahachal Marg, Kathmandu 44600, Nepal"},
    {"name": "Nasal Chowk", "address": "P834+MXP, Layaku Marg, Kathmandu 44600, Nepal"}
]

descriptions = []
for place in places:
    print(f"Fetching description for: {place['name']} ({place['address']})")
    description = get_wikipedia_summary(place['name'])
    descriptions.append({"name": place["name"], "address": place["address"], "description": description})
    print(f"Description: {description}\n")
    time.sleep(1)  # Sleep to avoid hitting API rate limits

# Save to JSON file
with open("description.json", "w", encoding="utf-8") as f:
    json.dump(descriptions, f, indent=4, ensure_ascii=False)
