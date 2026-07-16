from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.market import Market
from app.schemas.market import (
    MarketCreate,
    MarketUpdate,
    MarketResponse,
)

router = APIRouter(
    prefix="/markets",
    tags=["Markets"]
)


@router.post("/", response_model=MarketResponse)
def create_market(
    market: MarketCreate,
    db: Session = Depends(get_db)
):
    db_market = Market(
        name=market.name,
        open_time=market.open_time,
        close_time=market.close_time
    )

    db.add(db_market)
    db.commit()
    db.refresh(db_market)

    return db_market


@router.get("/", response_model=list[MarketResponse])
def get_markets(
    db: Session = Depends(get_db)
):
    return db.query(Market).all()


@router.get("/{market_id}", response_model=MarketResponse)
def get_market(
    market_id: int,
    db: Session = Depends(get_db)
):
    market = db.query(Market).filter(
        Market.id == market_id
    ).first()

    if market is None:
        raise HTTPException(
            status_code=404,
            detail="Market not found"
        )

    return market


@router.put("/{market_id}", response_model=MarketResponse)
def update_market(
    market_id: int,
    market: MarketUpdate,
    db: Session = Depends(get_db)
):
    db_market = db.query(Market).filter(
        Market.id == market_id
    ).first()

    if db_market is None:
        raise HTTPException(
            status_code=404,
            detail="Market not found"
        )

    db_market.name = market.name
    db_market.open_time = market.open_time
    db_market.close_time = market.close_time
    db_market.is_active = market.is_active

    db.commit()
    db.refresh(db_market)

    return db_market


@router.delete("/{market_id}")
def delete_market(
    market_id: int,
    db: Session = Depends(get_db)
):
    db_market = db.query(Market).filter(
        Market.id == market_id
    ).first()

    if db_market is None:
        raise HTTPException(
            status_code=404,
            detail="Market not found"
        )

    db.delete(db_market)
    db.commit()

    return {
        "message": "Market deleted successfully"
    }