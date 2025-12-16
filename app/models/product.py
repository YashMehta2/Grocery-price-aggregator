from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    store: str
    name: str
    price: Optional[float]
