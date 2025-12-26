GROCERY_STORES = {
    "Walmart",
    "Target",
    "Instacart"
}

NON_GROCERY_KEYWORDS = [
    "phone", "smartphone", "tv", "television",
    "laptop", "tablet", "computer",
    "headphone", "earbud", "speaker",
    "charger", "cable", "case",
    "monitor", "keyboard", "mouse",
    "appliance", "microwave", "refrigerator"
]

def normalize_store(store: str) -> str:
    if not store:
        return ""

    store = store.lower()

    if "walmart" in store:
        return "Walmart"
    if "target" in store:
        return "Target"
    if "instacart" in store:
        return "Instacart"

    return ""

def is_grocery_item(item: dict) -> bool:
    title = item.get("name", "").lower()
    store = normalize_store(item.get("store", ""))

    if store not in GROCERY_STORES:
        return False

    for word in NON_GROCERY_KEYWORDS:
        if word in title:
            return False

    return True
