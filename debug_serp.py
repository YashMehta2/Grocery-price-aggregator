import os
from serpapi import GoogleSearch
import json

SERP_API_KEY = os.getenv("SERPAPI_KEY")

params = {
    "engine": "google_shopping",
    "q": "milk",
    "hl": "en",
    "gl": "us",
    "google_domain": "google.com",
    "location": "United States",
    "api_key": SERP_API_KEY
}

search = GoogleSearch(params)
results = search.get_dict()

print("Raw Source Names in Google Shopping:")
for item in results.get("shopping_results", []):
    source = item.get("source", "")
    print(f"- {source}")

# Save full output for inspection
with open("dump.json", "w") as f:
    json.dump(results.get("shopping_results", []), f, indent=2)
