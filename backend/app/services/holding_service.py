from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.holding import Holding
from app.models.user import User
from app.schemas.holding import HoldingCreate, HoldingUpdate
from app.services.product_service import get_product


def list_holdings(db: Session, user: User) -> list[Holding]:
    return (
        db.query(Holding)
        .options(joinedload(Holding.product))
        .filter(Holding.user_id == user.id)
        .all()
    )


def get_holding(db: Session, holding_id: int, user: User) -> Holding:
    holding = (
        db.query(Holding)
        .options(joinedload(Holding.product))
        .filter(Holding.id == holding_id, Holding.user_id == user.id)
        .first()
    )
    if holding is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Holding not found")
    return holding


def create_holding(db: Session, payload: HoldingCreate, user: User) -> Holding:
    get_product(db, payload.product_id)
    holding = Holding(**payload.model_dump(), user_id=user.id)
    db.add(holding)
    db.commit()
    db.refresh(holding)
    return get_holding(db, holding.id, user)


def update_holding(db: Session, holding_id: int, payload: HoldingUpdate, user: User) -> Holding:
    holding = get_holding(db, holding_id, user)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(holding, key, value)
    db.commit()
    db.refresh(holding)
    return get_holding(db, holding.id, user)


def delete_holding(db: Session, holding_id: int, user: User) -> None:
    holding = get_holding(db, holding_id, user)
    db.delete(holding)
    db.commit()
