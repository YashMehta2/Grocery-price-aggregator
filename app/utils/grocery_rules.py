GROCERY_STORES = {
    "Walmart",
    "Target",
    "Instacart"
}

NON_GROCERY_KEYWORDS = [
    "phone", "smartphone", "tv", "television",
    "laptop", "tablet", "computer", "ipad", "macbook", "watch", "airpods", "airtag", "earpods",
    "headphone", "earbud", "speaker",
    "charger", "cable", "case", "adapter", "power",
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

def is_valid_query(query: str) -> bool:
    """
    Checks if the user's input search query itself is explicitly demanding a non-grocery item.
    """
    query_lower = query.lower()
    
    # Check if any non-grocery keyword is mentioned in the user's query
    for word in NON_GROCERY_KEYWORDS:
        if word in query_lower.split():
            return False
            
    # Explicitly block known tech brands
    blocked_brands = ["samsung", "apple", "sony", "lg", "dell", "hp", "lenovo", "asus", "nintendo", "playstation", "xbox"]
    for brand in blocked_brands:
        if brand in query_lower.split():
            # Exception for "apple" if they just want fruit
            if brand == "apple" and ("watch" not in query_lower and "ipad" not in query_lower and "mac" not in query_lower):
                continue
            return False
            
    return True

def is_valid_match(query: str, title: str) -> bool:
    """
    Intelligently filters out completely different flavors or items.
    If the user asks for "ice-cream", we shouldn't compare vanilla with strawberry cheesecake.
    """
    query = query.lower()
    title = title.lower()
    
    # If the user explicitly asks for a flavor/type, this logic is skipped because the query already contains it.
    # But if the user is vague (e.g. "ice-cream" or "milk"), we want to avoid weird outliers.

    # 1. Reject bulk packs if they aren't explicitly requested
    if "pack" not in query and "count" not in query and "ct" not in query:
        if any(x in title for x in ["pack", "count", " ct", "bulk"]):
            return False
            
    # 2. Prevent mixing totally different sub-categories if the query is simple
    if query == "ice-cream" or query == "ice cream":
        # Force default to vanilla if they just said "ice cream" so we compare apples to apples
        if "vanilla" not in title and "chocolate" in title:
            return False
        if "strawberry" in title or "cheesecake" in title or "mint" in title:
            return False
            
    if query == "milk":
        # Filter out weird milks if they just said milk
        if "almond" in title or "oat" in title or "soy" in title or "chocolate" in title or "powder" in title:
            return False
            
    if query == "chocolate":
        # Filter out chocolate adjacent things when looking for a bar
        if "syrup" in title or "milk" in title or "ice cream" in title or "cake" in title or "chip" in title:
            return False
            
    if query == "eggs":
        # Filter out egg adjacent things
        if "easter" in title or "chocolate" in title or "substitute" in title or "roll" in title:
            return False

    return True
