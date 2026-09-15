import re
with open('c:/Users/hmhar/Projects/Disaster_Coordinator/backend/agents/ingestion_agent.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Add imports
imports_addition = """import functools
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut"""

code = code.replace("import json", "import json\n" + imports_addition)

# Add class variable geolocator to IngestionAgent
init_addition = """
    def __init__(self):
        self.llm = get_llm("local", temperature=0.1)
        self.geolocator = Nominatim(user_agent="disaster_coordinator_geocoder")
"""
code = code.replace("""
    def __init__(self):
        self.llm = get_llm("local", temperature=0.1)""", init_addition)

# Add method to geocode
geocode_method = """
    @functools.lru_cache(maxsize=128)
    def _geocode_location(self, location_text: str) -> Optional[tuple[float, float]]:
        if not location_text or len(location_text) < 4 or location_text.lower() in ["unknown", "here", "help", "unknown (regex fallback)"]:
            return None
        try:
            # We don't want to spam or block forever
            location = self.geolocator.geocode(location_text, timeout=3)
            if location:
                return (location.latitude, location.longitude)
        except Exception:
            pass
        return None
"""

code = code.replace("    def _build_extracted_need", geocode_method + "\n    def _build_extracted_need")

# Replace coordinates=None with _geocode_location
code = code.replace(
    "coordinates=None, # Coordinates require geocoding, left None for now",
    "coordinates=self._geocode_location(llm_result.location_text),"
)

code = code.replace(
    "coordinates=None,",
    "coordinates=self._geocode_location(location),"
)

with open('c:/Users/hmhar/Projects/Disaster_Coordinator/backend/agents/ingestion_agent.py', 'w', encoding='utf-8') as f:
    f.write(code)
