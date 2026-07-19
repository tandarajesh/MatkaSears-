from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.result import Result
from app.models.game import Game
from app.schemas.result import (
    ResultCreate,
    ResultUpdate,
    ResultResponse,
)

router = APIRouter(
    prefix="/results",
    tags=["Results"]
)


@router.post("/", response_model=ResultResponse)
def create_result(
    result: ResultCreate,
    db: Session = Depends(get_db)
):
    game = db.query(Game).filter(
        Game.id == result.game_id
    ).first()

    if game is None:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    db_result = Result(
        game_id=result.game_id,
        result_date=result.result_date,
        open_result=result.open_result,
        close_result=result.close_result
    )

    db.add(db_result)
    db.commit()
    db.refresh(db_result)

    return db_result


@router.get("/", response_model=list[ResultResponse])
def get_results(
    db: Session = Depends(get_db)
):
    return db.query(Result).all()


@router.get("/{result_id}", response_model=ResultResponse)
def get_result(
    result_id: int,
    db: Session = Depends(get_db)
):
    result = db.query(Result).filter(
        Result.id == result_id
    ).first()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Result not found"
        )

    return result


@router.put("/{result_id}", response_model=ResultResponse)
def update_result(
    result_id: int,
    result: ResultUpdate,
    db: Session = Depends(get_db)
):
    db_result = db.query(Result).filter(
        Result.id == result_id
    ).first()

    if db_result is None:
        raise HTTPException(
            status_code=404,
            detail="Result not found"
        )

    db_result.game_id = result.game_id
    db_result.result_date = result.result_date
    db_result.open_result = result.open_result
    db_result.close_result = result.close_result

    db.commit()
    db.refresh(db_result)

    return db_result


@router.delete("/{result_id}")
def delete_result(
    result_id: int,
    db: Session = Depends(get_db)
):
    db_result = db.query(Result).filter(
        Result.id == result_id
    ).first()

    if db_result is None:
        raise HTTPException(
            status_code=404,
            detail="Result not found"
        )

    db.delete(db_result)
    db.commit()

    return {
        "message": "Result deleted successfully"
    }