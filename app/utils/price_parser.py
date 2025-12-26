import re
from typing import Optional

def parse_price(price_str: str) -> Optional[float]:
    """
    Converts price strings like:
    "$3.99", "USD 4.29", "$5", "$3.99 / lb"
    into float values.
    """
    if not price_str:
        return None

    # Extract first numeric value
    match = re.search(r"\d+(\.\d+)?", price_str.replace(",", ""))
    if not match:
        return None

    try:
        return float(match.group())
    except ValueError:
        return None
