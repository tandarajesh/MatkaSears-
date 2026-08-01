from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.wallet import Wallet
from app.models.user import User
from app.models.transaction import Transaction

from app.schemas.wallet import (
    WalletCreate,
    WalletUpdate,
    WalletResponse,
)


router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"]
)


@router.post("/", response_model=WalletResponse)
def create_wallet(
    wallet: WalletCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == wallet.user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing_wallet = db.query(Wallet).filter(
        Wallet.user_id == wallet.user_id
    ).first()

    if existing_wallet:
        raise HTTPException(
            status_code=400,
            detail="Wallet already exists"
        )

    db_wallet = Wallet(
        user_id=wallet.user_id,
        balance=0
    )

    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)

    return db_wallet


@router.get("/{user_id}", response_model=WalletResponse)
def get_wallet(
    user_id: int,
    db: Session = Depends(get_db)
):
    wallet = db.query(Wallet).filter(
        Wallet.user_id == user_id
    ).first()

    if wallet is None:
        raise HTTPException(
            status_code=404,
            detail="Wallet not found"
        )

    return wallet


@router.put(
    "/{user_id}/add-money",
    response_model=WalletResponse
)
def add_money(
    user_id: int,
    wallet: WalletUpdate,
    db: Session = Depends(get_db)
):
    db_wallet = db.query(Wallet).filter(
        Wallet.user_id == user_id
    ).first()

    if db_wallet is None:
        raise HTTPException(
            status_code=404,
            detail="Wallet not found"
        )

    db_wallet.balance += wallet.balance

    transaction = Transaction(
        user_id=user_id,
        transaction_type="Deposit",
        amount=wallet.balance,
        balance_after=db_wallet.balance,
        description="Wallet top-up"
    )

    db.add(transaction)

    db.commit()
    db.refresh(db_wallet)

    return db_wallet


@router.put(
    "/{user_id}/deduct-money",
    response_model=WalletResponse
)
def deduct_money(
    user_id: int,
    wallet: WalletUpdate,
    db: Session = Depends(get_db)
):
    db_wallet = db.query(Wallet).filter(
        Wallet.user_id == user_id
    ).first()

    if db_wallet is None:
        raise HTTPException(
            status_code=404,
            detail="Wallet not found"
        )

    if db_wallet.balance < wallet.balance:
        raise HTTPException(
            status_code=400,
            detail="Insufficient wallet balance"
        )

    db_wallet.balance -= wallet.balance

    transaction = Transaction(
        user_id=user_id,
        transaction_type="Withdrawal",
        amount=-wallet.balance,
        balance_after=db_wallet.balance,
        description="Wallet money deducted"
    )

    db.add(transaction)

    db.commit()
    db.refresh(db_wallet)

    return db_wallet