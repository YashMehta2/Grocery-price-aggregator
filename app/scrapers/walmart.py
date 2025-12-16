from playwright.sync_api import sync_playwright
import json

def search_walmart(query: str):
    url = f"https://www.walmart.com/search?q={query}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, timeout=30000)
        page.wait_for_selector('script#__NEXT_DATA__')

        script = page.locator('script#__NEXT_DATA__').inner_text()
        browser.close()

    data = json.loads(script)

    # Traverse JSON safely
    def find_items(obj):
        if isinstance(obj, dict):
            if "items" in obj and isinstance(obj["items"], list):
                return obj["items"]
            for v in obj.values():
                found = find_items(v)
                if found:
                    return found
        elif isinstance(obj, list):
            for i in obj:
                found = find_items(i)
                if found:
                    return found
        return []

    products = find_items(data)

    results = []
    for p in products[:8]:
        price = None
        if isinstance(p.get("priceInfo"), dict):
            price = p["priceInfo"].get("linePrice")

        results.append({
            "store": "Walmart",
            "name": p.get("name"),
            "price": price,
        })

    return results
