from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db

from app.models.user import User
from app.models.bet import Bet
from app.models.wallet import Wallet
from app.models.transaction import Transaction
from app.models.market import Market
from app.models.game import Game
from app.models.result import Result


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db)
):
    total_users = db.query(func.count(User.id)).scalar()

    total_bets = db.query(func.count(Bet.id)).scalar()

    total_markets = db.query(func.count(Market.id)).scalar()

    total_games = db.query(func.count(Game.id)).scalar()

    total_results = db.query(func.count(Result.id)).scalar()

    total_wallet_balance = db.query(
        func.sum(Wallet.balance)
    ).scalar() or 0

    return {
        "total_users": total_users,
        "total_bets": total_bets,
        "total_markets": total_markets,
        "total_games": total_games,
        "total_results": total_results,
        "total_wallet_balance": total_wallet_balance
    }