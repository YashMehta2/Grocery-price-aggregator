from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.services.best_price import (
    get_best_price,
    get_best_price_bulk
)

router = APIRouter(prefix="/api/best-price", tags=["Best Price"])


class BulkRequest(BaseModel):
    queries: List[str]


@router.get("/")
def best_price(query: str):
    """
    Example:
    /api/best-price?query=milk
    """
    return {
        "query": query,
        "best_option": get_best_price(query)
    }


@router.post("/bulk")
def best_price_bulk(payload: BulkRequest):
    """
    Example:
    POST /api/best-price/bulk
    {
        "queries": ["milk", "bread", "eggs"]
    }
    """
    return get_best_price_bulk(payload.queries)
