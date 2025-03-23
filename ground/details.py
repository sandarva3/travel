import requests
import time
import json
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Tuple
import concurrent.futures

class WikipediaDescriptionFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.common_variants = {
            'durbar': ['darbar', 'durbar', 'darvar', 'durvar'],
            'stupa': ['stupa', 'chaitya', 'chorten'],
            'temple': ['temple', 'mandir'],
            'swoyambhu': ['swayambhu', 'swayambhunath', 'swoyambhunath'],
            'square': ['square', 'chowk', 'chok']
        }
        
    def generate_name_variants(self, place_name: str) -> List[str]:
        """Generate possible variants of the place name."""
        variants = [place_name]
        lower_name = place_name.lower()
        
        # Add base name without any suffix
        base_name = place_name.split('-')[0].strip()
        if base_name != place_name:
            variants.append(base_name)
            
        # Check and replace known variants
        for key, alternatives in self.common_variants.items():
            if key in lower_name:
                for alt in alternatives:
                    new_variant = lower_name.replace(key, alt)
                    variants.append(new_variant.title())
        
        # Handle special cases for Nepali places
        if "darbar square" in lower_name or "durbar square" in lower_name:
            city = None
            for potential_city in ["patan", "kathmandu", "bhaktapur"]:
                if potential_city in lower_name:
                    city = potential_city
                    break
            if city:
                variants.extend([
                    f"{city.title()} Durbar Square",
                    f"{city.title()} Darbar Square",
                    f"{city.title()} Palace",
                    f"{city.title()} Palace Square"
                ])
        
        return list(set(variants))  # Remove duplicates

    def smart_wikipedia_search(self, place_name: str, address: str) -> Tuple[Optional[str], Optional[str]]:
        """Smart search with variants, returns (title, description)."""
        variants = self.generate_name_variants(place_name)
        
        # Extract city from address for context
        address_lower = address.lower()
        cities = ["kathmandu", "lalitpur", "patan", "bhaktapur"]
        city_context = next((city for city in cities if city in address_lower), None)
        
        best_title = None
        best_description = None
        best_similarity = 0.5  # Minimum threshold
        
        for variant in variants:
            search_term = f"{variant} {city_context}" if city_context else variant
            
            try:
                # Search Wikipedia
                search_url = "https://en.wikipedia.org/w/api.php"
                params = {
                    "action": "query",
                    "list": "search",
                    "srsearch": search_term,
                    "format": "json",
                    "srlimit": 3  # Limit to top 3 results
                }
                
                response = self.session.get(search_url, params=params)
                response.raise_for_status()
                data = response.json()
                search_results = data.get("query", {}).get("search", [])
                
                for result in search_results:
                    similarity = SequenceMatcher(None, variant.lower(), result['title'].lower()).ratio()
                    
                    # Check if this is a better match
                    if similarity > best_similarity:
                        # Try to get description
                        description = self.get_wikipedia_description(result['title'])
                        if description:
                            best_similarity = similarity
                            best_title = result['title']
                            best_description = description
                            
                            # If we find a very good match (>0.8), return immediately
                            if similarity > 0.8:
                                return best_title, best_description
                
                time.sleep(0.1)  # Small delay between variant searches
                
            except requests.RequestException:
                continue
        
        return best_title, best_description

    def get_wikipedia_description(self, title: str) -> Optional[str]:
        """Get detailed Wikipedia description."""
        params = {
            "action": "query",
            "prop": "extracts",
            "exintro": 1,
            "explaintext": 1,
            "titles": title,
            "format": "json"
        }
        
        try:
            response = self.session.get("https://en.wikipedia.org/w/api.php", params=params)
            response.raise_for_status()
            data = response.json()
            
            pages = data["query"]["pages"]
            page_id = next(iter(pages))
            return pages[page_id].get("extract")
            
        except (requests.RequestException, KeyError):
            return None

    def get_place_description(self, place: Dict) -> Dict:
        """Get description from Wikipedia using smart search."""
        name = place["name"]
        address = place["address"]
        
        # Try smart search with variants
        title, description = self.smart_wikipedia_search(name, address)
        
        if description:
            return {
                "name": name,
                "address": address,
                "description": description.strip()
            }
        
        return {
            "name": name,
            "address": address,
            "description": "No description available, even after fuzzy search mechanism."
        }

    def fetch_all_descriptions(self, places: List[Dict], max_workers: int = 5) -> List[Dict]:
        """Fetch descriptions for all places concurrently."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.get_place_description, places))
        return results

# Rest of your code remains the same...

def save_descriptions(descriptions: List[Dict], filename: str = "descriptions.json"):
    """Save descriptions to JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(descriptions, f, indent=4, ensure_ascii=False)

# Usage example
if __name__ == "__main__":
    # Initialize fetcher
    fetcher = WikipediaDescriptionFetcher()
    
    # Your places list here
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
    
    # Fetch descriptions
    descriptions = fetcher.fetch_all_descriptions(places)
    
    # Save results
    save_descriptions(descriptions)