from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)


router = APIRouter()

@router.get("/agent")
async def agent(request: str):

    # Create agent logic here.
    
    return { "response": f"{request} received!"}

app.include_router(router, prefix="/api")
