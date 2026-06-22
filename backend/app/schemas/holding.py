from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.product import ProductRead


class HoldingBase(BaseModel):
    product_id: int
    quantity: Decimal = Field(gt=0)
    average_price: Decimal = Field(gt=0)
    current_value: Decimal = Field(ge=0)


class HoldingCreate(HoldingBase):
    pass


class HoldingUpdate(BaseModel):
    quantity: Decimal | None = Field(default=None, gt=0)
    average_price: Decimal | None = Field(default=None, gt=0)
    current_value: Decimal | None = Field(default=None, ge=0)


class HoldingRead(HoldingBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    product: ProductRead

    model_config = ConfigDict(from_attributes=True)
