from fastapi import FastAPI

from app.db.database import Base, engine
from app.models.user import User
from app.models.market import Market
from app.models.game import Game
from app.models.result import Result
from app.models.bet import Bet
from app.models.wallet import Wallet
from app.models.prize_multiplier import PrizeMultiplier
from app.models.transaction import Transaction

from app.api.user import router as user_router
from app.api.market import router as market_router
from app.api.game import router as game_router
from app.api.result import router as result_router
from app.api.bet import router as bet_router
from app.api.wallet import router as wallet_router
from app.api.prize_multiplier import router as prize_multiplier_router
from app.api.transaction import router as transaction_router
from app.api import admin


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
app.include_router(wallet_router)
app.include_router(prize_multiplier_router)
app.include_router(transaction_router)

app.include_router(admin.router)


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