from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.game import Game
from app.models.market import Market
from app.schemas.game import (
    GameCreate,
    GameUpdate,
    GameResponse,
)

router = APIRouter(
    prefix="/games",
    tags=["Games"]
)


@router.post("/", response_model=GameResponse)
def create_game(
    game: GameCreate,
    db: Session = Depends(get_db)
):
    market = db.query(Market).filter(
        Market.id == game.market_id
    ).first()

    if market is None:
        raise HTTPException(
            status_code=404,
            detail="Market not found"
        )

    db_game = Game(
        market_id=game.market_id,
        name=game.name,
        open_time=game.open_time,
        close_time=game.close_time
    )

    db.add(db_game)
    db.commit()
    db.refresh(db_game)

    return db_game


@router.get("/", response_model=list[GameResponse])
def get_games(
    db: Session = Depends(get_db)
):
    return db.query(Game).all()


@router.get("/{game_id}", response_model=GameResponse)
def get_game(
    game_id: int,
    db: Session = Depends(get_db)
):
    game = db.query(Game).filter(
        Game.id == game_id
    ).first()

    if game is None:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    return game


@router.put("/{game_id}", response_model=GameResponse)
def update_game(
    game_id: int,
    game: GameUpdate,
    db: Session = Depends(get_db)
):
    db_game = db.query(Game).filter(
        Game.id == game_id
    ).first()

    if db_game is None:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    db_game.market_id = game.market_id
    db_game.name = game.name
    db_game.open_time = game.open_time
    db_game.close_time = game.close_time
    db_game.is_active = game.is_active

    db.commit()
    db.refresh(db_game)

    return db_game


@router.delete("/{game_id}")
def delete_game(
    game_id: int,
    db: Session = Depends(get_db)
):
    db_game = db.query(Game).filter(
        Game.id == game_id
    ).first()

    if db_game is None:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    db.delete(db_game)
    db.commit()

    return {
        "message": "Game deleted successfully"
    }