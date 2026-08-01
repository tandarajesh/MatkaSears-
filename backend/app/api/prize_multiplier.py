from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.prize_multiplier import PrizeMultiplier
from app.schemas.prize_multiplier import (
    PrizeMultiplierCreate,
    PrizeMultiplierUpdate,
    PrizeMultiplierResponse,
)

router = APIRouter(
    prefix="/prize-multipliers",
    tags=["Prize Multipliers"]
)


@router.post("/", response_model=PrizeMultiplierResponse)
def create_prize_multiplier(
    prize: PrizeMultiplierCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(PrizeMultiplier).filter(
        PrizeMultiplier.bet_type == prize.bet_type
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Bet type already exists"
        )

    db_prize = PrizeMultiplier(
        bet_type=prize.bet_type,
        multiplier=prize.multiplier
    )

    db.add(db_prize)
    db.commit()
    db.refresh(db_prize)

    return db_prize


@router.get("/", response_model=list[PrizeMultiplierResponse])
def get_prize_multipliers(
    db: Session = Depends(get_db)
):
    return db.query(PrizeMultiplier).all()


@router.get("/{prize_id}", response_model=PrizeMultiplierResponse)
def get_prize_multiplier(
    prize_id: int,
    db: Session = Depends(get_db)
):
    prize = db.query(PrizeMultiplier).filter(
        PrizeMultiplier.id == prize_id
    ).first()

    if prize is None:
        raise HTTPException(
            status_code=404,
            detail="Prize multiplier not found"
        )

    return prize


@router.put("/{prize_id}", response_model=PrizeMultiplierResponse)
def update_prize_multiplier(
    prize_id: int,
    prize: PrizeMultiplierUpdate,
    db: Session = Depends(get_db)
):
    db_prize = db.query(PrizeMultiplier).filter(
        PrizeMultiplier.id == prize_id
    ).first()

    if db_prize is None:
        raise HTTPException(
            status_code=404,
            detail="Prize multiplier not found"
        )

    db_prize.bet_type = prize.bet_type
    db_prize.multiplier = prize.multiplier

    db.commit()
    db.refresh(db_prize)

    return db_prize


@router.delete("/{prize_id}")
def delete_prize_multiplier(
    prize_id: int,
    db: Session = Depends(get_db)
):
    db_prize = db.query(PrizeMultiplier).filter(
        PrizeMultiplier.id == prize_id
    ).first()

    if db_prize is None:
        raise HTTPException(
            status_code=404,
            detail="Prize multiplier not found"
        )

    db.delete(db_prize)
    db.commit()

    return {
        "message": "Prize multiplier deleted successfully"
    }