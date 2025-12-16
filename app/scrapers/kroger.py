import httpx

BASE_URL = "https://www.kroger.com/atlas/v1/product/v2/products"

def search_kroger(query: str, zip_code="10001"):
    params = {
        "term": query,
        "limit": 10,
        "locationId": zip_code
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    r = httpx.get(BASE_URL, params=params, headers=headers, timeout=10)
    data = r.json()

    results = []
    for p in data.get("data", []):
        item = p.get("items", [{}])[0]
        price = item.get("price", {}).get("regular")

        results.append({
            "store": "Kroger",
            "name": p.get("description"),
            "price": price,
        })

    return results
