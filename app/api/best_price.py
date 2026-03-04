from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

from app.services.best_price import (
    get_best_price,
    get_best_price_bulk
)
from app.services.email_service import send_best_price_email

router = APIRouter(prefix="/api/best-price", tags=["Best Price"])


class BulkRequest(BaseModel):
    queries: List[str]
    email: Optional[str] = None


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
        "queries": ["milk", "bread", "eggs"],
        "email": "user@example.com"
    }
    """
    results = get_best_price_bulk(payload.queries)
    
    email_sent = False
    if payload.email:
        email_sent = send_best_price_email(payload.email, results)
        
    return {
        "results": results,
        "email_sent": email_sent
    }
