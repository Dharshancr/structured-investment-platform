from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ProductBase(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    issuer: str = Field(min_length=2, max_length=255)
    underlying_asset: str = Field(min_length=1, max_length=255)
    product_type: str = Field(min_length=2, max_length=120)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    coupon_rate: Decimal = Field(ge=0)
    barrier_level: Decimal | None = Field(default=None, ge=0)
    strike_price: Decimal = Field(gt=0)
    issue_date: date
    maturity_date: date
    risk_rating: str = Field(min_length=2, max_length=50)
    description: str | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.maturity_date <= self.issue_date:
            raise ValueError("maturity_date must be after issue_date")
        return self


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    issuer: str | None = Field(default=None, min_length=2, max_length=255)
    underlying_asset: str | None = Field(default=None, min_length=1, max_length=255)
    product_type: str | None = Field(default=None, min_length=2, max_length=120)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    coupon_rate: Decimal | None = Field(default=None, ge=0)
    barrier_level: Decimal | None = Field(default=None, ge=0)
    strike_price: Decimal | None = Field(default=None, gt=0)
    issue_date: date | None = None
    maturity_date: date | None = None
    risk_rating: str | None = Field(default=None, min_length=2, max_length=50)
    description: str | None = None


class ProductRead(ProductBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
