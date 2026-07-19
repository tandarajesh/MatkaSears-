from fastapi import FastAPI

from app.db.database import Base, engine
from app.models.user import User
from app.models.market import Market
from app.models.game import Game
from app.models.result import Result
from app.models.bet import Bet

from app.api.user import router as user_router
from app.api.market import router as market_router
from app.api.game import router as game_router
from app.api.result import router as result_router
from app.api.bet import router as bet_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MatkaSears API",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(market_router)
app.include_router(game_router)
app.include_router(result_router)
app.include_router(bet_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to MatkaSears API",
        "status": "Running"
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }