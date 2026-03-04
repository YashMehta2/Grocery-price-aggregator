from app.services.aggregator import aggregate_prices
from app.utils.price_parser import parse_price

def get_best_price(query: str):
    products = aggregate_prices(query)
    
    # Check if the query was explicitly rejected due to being a non-grocery item
    if isinstance(products, dict) and products.get("error") == "blocked_category":
        return {"error": "blocked_category"}

    # Track all valid items per store
    store_items = {}

    for item in products:
        store = item.get("store")
        price = parse_price(item.get("price"))
        
        if price is None or not store:
            continue
            
        # Store the parsed price for easy sorting
        item['parsed_price'] = price

        if store not in store_items:
            store_items[store] = []
        
        # Avoid duplicate items (same name, same price)
        is_duplicate = any(
            existing.get("name") == item.get("name") and existing.get("parsed_price") == item.get("parsed_price")
            for existing in store_items[store]
        )
        if not is_duplicate:
            store_items[store].append(item)

    # Sort each store's items by price and keep top 3
    results_by_store = {}
    highest_price = 0
    lowest_price = float("inf")
    best_overall_store = None
    
    for store, items in store_items.items():
        # Sort ascending by price
        sorted_items = sorted(items, key=lambda x: x['parsed_price'])
        
        # Keep top 3
        top_3 = sorted_items[:3]
        results_by_store[store] = top_3
        
        # We calculate the savings based on the #1 cheapest item from each store
        if top_3:
            cheapest_in_store = top_3[0]['parsed_price']
            
            if cheapest_in_store > highest_price:
                highest_price = cheapest_in_store
                
            if cheapest_in_store < lowest_price:
                lowest_price = cheapest_in_store
                best_overall_store = store

    # Calculate savings compared to highest available starting price
    savings_amount = 0
    savings_percentage = 0
    
    if highest_price > 0 and lowest_price != float("inf"):
        savings_amount = round(highest_price - lowest_price, 2)
        savings_percentage = round((savings_amount / highest_price) * 100, 1)

    return {
        "prices_by_store": results_by_store,
        "best_overall": {
            "store": best_overall_store,
            "lowest_price": lowest_price if lowest_price != float("inf") else None,
            "savings_amount": savings_amount,
            "savings_percentage": savings_percentage
        } if best_overall_store else None
    }


def get_best_price_bulk(queries: list[str]):
    results = []

    for query in queries:
        query = query.strip()
        if not query:
            continue
            
        best = get_best_price(query)
        results.append({
            "query": query,
            "best_option": best
        })

    return results
