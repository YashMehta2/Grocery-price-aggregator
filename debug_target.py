import os
import json
from serpapi import GoogleSearch

SERP_API_KEY = os.getenv("SERPAPI_KEY")

queries_to_try = [
    "carrots site:target.com",
    "carrots target",
    "target grocery carrots",
    "carrots instacart target",
]

for q in queries_to_try:
    params = {
        "engine": "google_shopping",
        "q": q,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "location": "United States",
        "api_key": SERP_API_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    items = results.get("shopping_results", [])
    print(f"\nQuery: {q} -> Found {len(items)} items")
    if items:
        for item in items[:3]:
            print(f"  - {item.get('source')}: {item.get('title')}")
