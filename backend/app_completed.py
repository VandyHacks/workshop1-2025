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

def get_stock_prices(ticker: str, period: str) -> list:
    """
    Retrieves stock prices.
    Args:
        ticker: A valid ticker on the US exchange.
        period: Period from which to retreive data, must "Day" or "Week".
    Returns:
        A list of prices.
    """

    period2 = datetime.now()
    if period == "Day":
        period1 = period2 - timedelta(days=1)
    if period == "Week":
        period1 = period2 - timedelta(weeks=1)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={int(period1.timestamp())}&period2={int(period2.timestamp())}&interval=30m&lang=en-US&region=US"
    response = requests.get(url, headers=headers).json()
    return [round(_, 2) for _ in response["chart"]["result"][0]["indicators"]["quote"][0]["open"]]


client = genai.Client(api_key="AIzaSyBu_2DhppbkSN7kfIUhAkvvBjIpTTWjLVo")
config = types.GenerateContentConfig(
    system_instruction="You are an AI analyst that examines stock market data. Do not include a list of prices your response. Make the response very long.",
    tools=[get_stock_prices]
)

@router.get("/agent")
async def agent(request: str):

    # Create agent logic here.
    content = [
        types.Content(role="user", parts=[types.Part(text=request)])
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=content,
        config=config
    )
    
    return { "response": response.text }

app.include_router(router, prefix="/api")
