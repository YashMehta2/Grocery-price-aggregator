from serpapi import GoogleSearch
import os
from app.utils.grocery_rules import GROCERY_STORES, normalize_store

SERP_API_KEY = os.getenv("SERPAPI_KEY")

def search_products(query: str):
    products = []
    
    # We must explicitly query the stores, otherwise Google Shopping fills with Instacart and random local stores
    search_queries = [
        (f"{query} walmart", "Walmart"), # Organic keyword instead of site:
        (f"{query} target", "Target"), # Target often fails with site:target.com
        (f"{query} instacart", "Instacart")
    ]
    
    for search_term, expected_store in search_queries:
        params = {
            "engine": "google_shopping",
            "q": search_term,
            "hl": "en",
            "gl": "us",
            "google_domain": "google.com",
            "location": "United States",
            "api_key": SERP_API_KEY
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            for item in results.get("shopping_results", []):
                store_raw = item.get("source", "")
                store = normalize_store(store_raw)
                
                # If Google doesn't return the strict source name but we know we forced it via site operator:
                if not store and expected_store.lower() in store_raw.lower():
                    store = expected_store
                elif not store:
                    # Fallback if source is completely missing but we searched via site:
                    store = expected_store

                if store not in GROCERY_STORES:
                    continue

                products.append({
                    "store": store,
                    "name": item.get("title"),
                    "price": item.get("price"),
                    "link": item.get("link"),
                    "thumbnail": item.get("thumbnail")
                })
        except Exception as e:
            print(f"Error searching for {search_term}: {e}")

    return products
