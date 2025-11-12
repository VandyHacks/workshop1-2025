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

router = APIRouter()

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
# }
# url = f"https://query1.finance.yahoo.com/v8/finance/chart/AAPL?period1=1762973017&period2=1762974017&interval=30m&lang=en-US&region=US"

def get_stock_prices(ticker: str, period: str) -> list:
    """
    Retrieves stock prices from a specified time period.

    Args:
        ticker: A valid ticker listed on a US exchange.
        period: Period from which to retreive data, must be "Day" or "Week".
    
    Returns:
        A list of prices from the specified time period in a 30 minute interval.
    """

    period2 = datetime.now()
    if period == "Day":
        period1 = period2 - timedelta(days=1)
    else:
        period1 = period2 - timedelta(weeks=1)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }
    response = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={int(period1.timestamp())}&period2={int(period2.timestamp())}&interval=30m&lang=en-US&region=US", headers=headers).json()
    return [round(_, 2) for _ in response["chart"]["result"][0]["indicators"]["quote"][0]["open"]]


client = genai.Client(api_key="AIzaSyB2S3ivT3aq_C8y5Gg-eJOdyhKk0wFiHFc")
config = types.GenerateContentConfig(
    system_instruction="You are an AI analyst that examines stock market data to identify trends and patterns. Be verbose with your responses. Do not include a list of prices in your response.",
    tools=[get_stock_prices],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
)

@router.get("/agent")
async def agent(request: str):

    contents = [
        types.Content(role="user", parts=[types.Part(text=request)])
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=config,
    )

    tool_call = response.candidates[0].content.parts[0].function_call #type: ignore

    if not tool_call:
        return {"response": response.text}

    if tool_call.name == "get_stock_prices":
        result = get_stock_prices(**tool_call.args) #type: ignore

    contents.append(types.Content(role="model", parts=[types.Part.from_function_call(
        name=tool_call.name, #type: ignore
        args=tool_call.args  #type: ignore
    )]))
    contents.append(types.Content(role="user", parts=[types.Part.from_function_response(
        name=tool_call.name, #type: ignore
        response={"result": result}
    )]))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=config,
    )

    return {"response": response.text }

app.include_router(router, prefix="/api")