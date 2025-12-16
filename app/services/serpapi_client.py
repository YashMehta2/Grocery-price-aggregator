from serpapi import GoogleSearch
import os

SERP_API_KEY = os.getenv("SERPAPI_KEY")

def search_products(query: str):
    params = {
        "engine": "google_shopping",
        "q": query,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "location": "United States",
        "device": "desktop",
        "api_key": SERP_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # 🔍 DEBUG: print raw response once
    print("SERPAPI RAW RESPONSE:", results)
    print("SERPAPI_KEY =", SERP_API_KEY)

    products = []

    for item in results.get("shopping_results", []):
        products.append({
            "store": item.get("source"),
            "name": item.get("title"),
            "price": item.get("price"),
        })

    return products
