from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.result import Result
from app.models.market import Market
from app.models.game import Game
from app.models.bet import Bet
from app.models.wallet import Wallet
from app.models.transaction import Transaction
from app.models.prize_multiplier import PrizeMultiplier

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
    market = db.query(Market).filter(
        Market.id == result.market_id
    ).first()

    if market is None:
        raise HTTPException(
            status_code=404,
            detail="Market not found"
        )

    game = db.query(Game).filter(
        Game.id == result.game_id
    ).first()

    if game is None:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    db_result = Result(
        market_id=result.market_id,
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
    db_result.market_id = result.market_id
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


def process_winning_bet(
    db: Session,
    bet: Bet,
    multiplier_name: str,
    description: str,
    total_winners: int,
    total_payout: int
):
    prize = db.query(PrizeMultiplier).filter(
        PrizeMultiplier.bet_type == multiplier_name
    ).first()

    if prize is None:
        return total_winners, total_payout

    wallet = db.query(Wallet).filter(
        Wallet.user_id == bet.user_id
    ).first()

    if wallet is None:
        return total_winners, total_payout

    win_amount = bet.points * prize.multiplier

    wallet.balance += win_amount

    transaction = Transaction(
        user_id=bet.user_id,
        transaction_type="Win",
        amount=win_amount,
        balance_after=wallet.balance,
        description=description
    )

    db.add(transaction)

    bet.status = "Won"

    total_winners += 1
    total_payout += win_amount

    return total_winners, total_payout

@router.post("/{result_id}/process")
def process_result(
    result_id: int,
    db: Session = Depends(get_db)
):
    # Find result
    result = db.query(Result).filter(
        Result.id == result_id
    ).first()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Result not found"
        )

    # Prevent duplicate processing
    if result.processed:
        raise HTTPException(
            status_code=400,
            detail="Result already processed"
        )

    # Find all matching bets
    bets = db.query(Bet).filter(
        Bet.market_id == result.market_id,
        Bet.game_id == result.game_id,
        Bet.bet_date == result.result_date
    ).all()

    total_winners = 0
    total_payout = 0

    # Process every bet
    for bet in bets:

        # Default status
        bet.status = "Lost"

        # =========================
        # OPEN SINGLE
        # =========================
        if (
            bet.bet_type == "Open Single"
            and bet.number == result.open_result
        ):

            total_winners, total_payout = process_winning_bet(
                db=db,
                bet=bet,
                multiplier_name="Open Single",
                description="Open Single Winning",
                total_winners=total_winners,
                total_payout=total_payout
            )

        # =========================
        # CLOSE SINGLE
        # =========================
        if (
            bet.bet_type == "Close Single"
            and bet.number == result.close_result
        ):

            total_winners, total_payout = process_winning_bet(
                db=db,
                bet=bet,
                multiplier_name="Close Single",
                description="Close Single Winning",
                total_winners=total_winners,
                total_payout=total_payout
           )
            
        # =========================
        # JODI
        # =========================
        if (
            bet.bet_type == "Jodi"
            and bet.number == (result.open_result + result.close_result)
        ):

            total_winners, total_payout = process_winning_bet(
                db=db,
                bet=bet,
                multiplier_name="Jodi",
                description="Jodi Winning",
                total_winners=total_winners,
                total_payout=total_payout
           )
       
       
        # =========================
        # OPEN PATTI
        # =========================
        if (
            bet.bet_type == "Open Patti"
            and bet.number == result.open_result
        ):

            total_winners, total_payout = process_winning_bet(
                db=db,
                bet=bet,
                multiplier_name="Open Patti",
                description="Open Patti Winning",
                total_winners=total_winners,
                total_payout=total_payout
           )

        # =========================
        # CLOSE PATTI
        # =========================
        if (
            bet.bet_type == "Close Patti"
            and bet.number == result.close_result
        ):

            total_winners, total_payout = process_winning_bet(
                db=db,
                bet=bet,
                multiplier_name="Close Patti",
                description="Close Patti Winning",
                total_winners=total_winners,
                total_payout=total_payout
           )

        # =========================
        # HALF SANGAM
        # =========================
        if (
            bet.bet_type == "Half Sangam"
            and bet.number == (result.open_result + result.close_result)
        ):

            total_winners, total_payout = process_winning_bet(
                db=db,
                bet=bet,
                multiplier_name="Half Sangam",
                description="Half Sangam Winning",
                total_winners=total_winners,
                total_payout=total_payout
           )
           
        # =========================
        # FULL SANGAM
        # =========================
        if (
            bet.bet_type == "Full Sangam"
            and bet.number == (result.open_result + result.close_result)
        ):

            total_winners, total_payout = process_winning_bet(
                db=db,
                bet=bet,
                multiplier_name="Full Sangam",
                description="Full Sangam Winning",
                total_winners=total_winners,
                total_payout=total_payout
           )


    # Mark result as processed
    result.processed = True

    # Save everything
    db.commit()

    return {
        "message": "Result processed successfully",
        "result_id": result.id,
        "total_bets": len(bets),
        "total_winners": total_winners,
        "total_payout": total_payout
    }