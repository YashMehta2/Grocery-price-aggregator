from app.services.serpapi_client import search_products
from app.utils.grocery_rules import is_grocery_item, is_valid_match, is_valid_query

def aggregate_prices(query: str):
    if not is_valid_query(query):
        return {"error": "blocked_category"}
        
    results = search_products(query)
    
    valid_products = []
    for item in results:
        if is_grocery_item(item) and is_valid_match(query, item.get("name", "")):
            valid_products.append(item)
            
    return valid_products
