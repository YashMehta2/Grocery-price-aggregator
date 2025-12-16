from app.services.serpapi_client import search_products
from app.utils.grocery_rules import is_grocery_item

def aggregate_prices(query: str):
    results = search_products(query)
    return [item for item in results if is_grocery_item(item)]
