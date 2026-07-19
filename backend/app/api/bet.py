from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.bet import Bet
from app.models.user import User
from app.models.market import Market
from app.models.game import Game
from app.schemas.bet import (
    BetCreate,
    BetUpdate,
    BetResponse,
)

router = APIRouter(
    prefix="/bets",
    tags=["Bets"]
)


@router.post("/", response_model=BetResponse)
def create_bet(
    bet: BetCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == bet.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    market = db.query(Market).filter(Market.id == bet.market_id).first()
    if market is None:
        raise HTTPException(status_code=404, detail="Market not found")

    game = db.query(Game).filter(Game.id == bet.game_id).first()
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    db_bet = Bet(
        user_id=bet.user_id,
        market_id=bet.market_id,
        game_id=bet.game_id,
        bet_type=bet.bet_type,
        number=bet.number,
        points=bet.points,
        bet_date=bet.bet_date,
    )

    db.add(db_bet)
    db.commit()
    db.refresh(db_bet)

    return db_bet


@router.get("/", response_model=list[BetResponse])
def get_bets(db: Session = Depends(get_db)):
    return db.query(Bet).all()


@router.get("/{bet_id}", response_model=BetResponse)
def get_bet(
    bet_id: int,
    db: Session = Depends(get_db)
):
    bet = db.query(Bet).filter(Bet.id == bet_id).first()

    if bet is None:
        raise HTTPException(
            status_code=404,
            detail="Bet not found"
        )

    return bet


@router.put("/{bet_id}", response_model=BetResponse)
def update_bet(
    bet_id: int,
    bet: BetUpdate,
    db: Session = Depends(get_db)
):
    db_bet = db.query(Bet).filter(Bet.id == bet_id).first()

    if db_bet is None:
        raise HTTPException(
            status_code=404,
            detail="Bet not found"
        )

    db_bet.user_id = bet.user_id
    db_bet.market_id = bet.market_id
    db_bet.game_id = bet.game_id
    db_bet.bet_type = bet.bet_type
    db_bet.number = bet.number
    db_bet.points = bet.points
    db_bet.bet_date = bet.bet_date
    db_bet.status = bet.status

    db.commit()
    db.refresh(db_bet)

    return db_bet


@router.delete("/{bet_id}")
def delete_bet(
    bet_id: int,
    db: Session = Depends(get_db)
):
    db_bet = db.query(Bet).filter(Bet.id == bet_id).first()

    if db_bet is None:
        raise HTTPException(
            status_code=404,
            detail="Bet not found"
        )

    db.delete(db_bet)
    db.commit()

    return {
        "message": "Bet deleted successfully"
    }