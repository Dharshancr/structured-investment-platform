from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.product import ProductRead


TransactionType = Literal["BUY", "SELL", "COUPON", "REDEMPTION"]


class TransactionBase(BaseModel):
    product_id: int
    transaction_type: TransactionType
    quantity: Decimal = Field(gt=0)
    price: Decimal = Field(ge=0)
    fees: Decimal = Field(default=0, ge=0)
    executed_at: datetime | None = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    transaction_type: TransactionType | None = None
    quantity: Decimal | None = Field(default=None, gt=0)
    price: Decimal | None = Field(default=None, ge=0)
    fees: Decimal | None = Field(default=None, ge=0)
    executed_at: datetime | None = None


class TransactionRead(TransactionBase):
    id: int
    user_id: int
    executed_at: datetime
    product: ProductRead

    model_config = ConfigDict(from_attributes=True)
