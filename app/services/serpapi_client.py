from serpapi import GoogleSearch
import os
from app.utils.grocery_rules import GROCERY_STORES, normalize_store

SERP_API_KEY = os.getenv("SERPAPI_KEY")

def search_products(query: str):
    params = {
        "engine": "google_shopping",
        "q": query,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "location": "United States",
        "api_key": SERP_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    products = []

    for item in results.get("shopping_results", []):
        store_raw = item.get("source", "")
        store = normalize_store(store_raw)

        if store not in GROCERY_STORES:
            continue

        products.append({
            "store": store,
            "name": item.get("title"),
            "price": item.get("price"),
            "link": item.get("link"),
            "thumbnail": item.get("thumbnail")
        })

    return products
