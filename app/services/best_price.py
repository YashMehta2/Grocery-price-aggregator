from app.services.aggregator import aggregate_prices
from app.utils.price_parser import parse_price

def get_best_price(query: str):
    products = aggregate_prices(query)

    best_item = None
    best_price = float("inf")

    for item in products:
        price = parse_price(item.get("price"))
        if price is None:
            continue

        if price < best_price:
            best_price = price
            best_item = item

    return best_item


def get_best_price_bulk(queries: list[str]):
    results = []

    for query in queries:
        best = get_best_price(query)
        results.append({
            "query": query,
            "best_option": best
        })

    return results
