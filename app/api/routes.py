from fastapi import APIRouter, Query
from app.services.aggregator import aggregate_prices

router = APIRouter(prefix="/api")

@router.get("/search")
def search_products(
    query: str = Query(..., min_length=2)
):
    results = aggregate_prices(query)
    return {
        "query": query,
        "count": len(results),
        "results": results
    }
