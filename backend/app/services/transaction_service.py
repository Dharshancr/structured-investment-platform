from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.services.product_service import get_product


def list_transactions(db: Session, user: User) -> list[Transaction]:
    return (
        db.query(Transaction)
        .options(joinedload(Transaction.product))
        .filter(Transaction.user_id == user.id)
        .order_by(Transaction.executed_at.desc())
        .all()
    )


def get_transaction(db: Session, transaction_id: int, user: User) -> Transaction:
    transaction = (
        db.query(Transaction)
        .options(joinedload(Transaction.product))
        .filter(Transaction.id == transaction_id, Transaction.user_id == user.id)
        .first()
    )
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction


def create_transaction(db: Session, payload: TransactionCreate, user: User) -> Transaction:
    get_product(db, payload.product_id)
    data = payload.model_dump(exclude_none=True)
    transaction = Transaction(**data, user_id=user.id)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return get_transaction(db, transaction.id, user)


def update_transaction(db: Session, transaction_id: int, payload: TransactionUpdate, user: User) -> Transaction:
    transaction = get_transaction(db, transaction_id, user)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(transaction, key, value)
    db.commit()
    db.refresh(transaction)
    return get_transaction(db, transaction.id, user)


def delete_transaction(db: Session, transaction_id: int, user: User) -> None:
    transaction = get_transaction(db, transaction_id, user)
    db.delete(transaction)
    db.commit()
