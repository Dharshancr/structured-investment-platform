from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlalchemy import Date, DateTime, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    issuer: Mapped[str] = mapped_column(String(255), nullable=False)
    underlying_asset: Mapped[str] = mapped_column(String(255), nullable=False)
    product_type: Mapped[str] = mapped_column(String(120), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    coupon_rate: Mapped[Decimal] = mapped_column(Numeric(8, 4), nullable=False)
    barrier_level: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 4), nullable=True)
    strike_price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    maturity_date: Mapped[date] = mapped_column(Date, nullable=False)
    risk_rating: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    holdings = relationship("Holding", back_populates="product")
    transactions = relationship("Transaction", back_populates="product")
