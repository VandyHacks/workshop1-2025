from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
import requests
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
# }
# url = f"https://query1.finance.yahoo.com/v8/finance/chart/AAPL?period1=1762973017&period2=1762974017&interval=30m&lang=en-US&region=US"

router = APIRouter()

@router.get("/agent")
async def agent(request: str):

    # Create agent logic here.
    
    return { "response": f"{request} received!"}

app.include_router(router, prefix="/api")