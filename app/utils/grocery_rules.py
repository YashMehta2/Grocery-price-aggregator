GROCERY_STORES = {
    "Walmart",
    "Kroger",
    "Costco"
}

NON_GROCERY_KEYWORDS = [
    "phone", "smartphone", "tv", "television",
    "laptop", "tablet", "computer",
    "headphone", "earbud", "speaker",
    "charger", "cable", "case",
    "monitor", "keyboard", "mouse",
    "appliance", "microwave", "refrigerator"
]

def is_grocery_item(item: dict) -> bool:
    title = item.get("name", "").lower()
    store = item.get("store", "")

    # Rule 1: Store whitelist
    if store not in GROCERY_STORES:
        return False

    # Rule 2: Block obvious non-grocery items
    for word in NON_GROCERY_KEYWORDS:
        if word in title:
            return False

    # Rule 3: Everything else from grocery stores = grocery
    return True
