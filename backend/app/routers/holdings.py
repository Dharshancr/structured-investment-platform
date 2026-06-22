from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.holding import HoldingCreate, HoldingRead, HoldingUpdate
from app.services import holding_service
from app.utils.dependencies import get_current_user

router = APIRouter()


@router.get("", response_model=list[HoldingRead])
def list_holdings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return holding_service.list_holdings(db, current_user)


@router.get("/{holding_id}", response_model=HoldingRead)
def get_holding(holding_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return holding_service.get_holding(db, holding_id, current_user)


@router.post("", response_model=HoldingRead, status_code=status.HTTP_201_CREATED)
def create_holding(
    payload: HoldingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return holding_service.create_holding(db, payload, current_user)


@router.patch("/{holding_id}", response_model=HoldingRead)
def update_holding(
    holding_id: int,
    payload: HoldingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return holding_service.update_holding(db, holding_id, payload, current_user)


@router.delete("/{holding_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_holding(holding_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    holding_service.delete_holding(db, holding_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
