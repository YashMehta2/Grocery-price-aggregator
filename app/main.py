from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.api.routes import router
from app.api.best_price import router as best_price_router

app = FastAPI()

# Existing search API
app.include_router(router, prefix="/api")

# Best price API
app.include_router(best_price_router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "API is running"}
