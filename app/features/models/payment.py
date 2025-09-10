from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, Enum, Numeric, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from ...core.db import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    type: Mapped[str] = mapped_column(Enum('credit', 'debit', name='payment_type'), nullable=False)
    sub_type: Mapped[str] = mapped_column(Enum('purchase', 'deposit', 'refund', name='payment_sub_type'), nullable=False)
    transaction_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(Enum('success', 'failed', 'pending', name='payment_status'), default='pending')
    external_system_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    external_system_transaction_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    channel: Mapped[str] = mapped_column(Enum('credit_card', 'debit_card', 'net_banking', 'wallet', 'upi', 'cash', name='payment_channel'), nullable=False)
    source_type: Mapped[str] = mapped_column(Enum('user', 'company', name='source_type'), nullable=False)
    source_id: Mapped[str] = mapped_column(String(36), nullable=False)
    destination_type: Mapped[str] = mapped_column(Enum('user', 'company', name='destination_type'), nullable=False)
    destination_id: Mapped[str] = mapped_column(String(36), nullable=False)
    additional_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    added_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    modified_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=datetime.utcnow)
    added_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    modified_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    user_payments: Mapped[list["UserPayment"]] = relationship("UserPayment", back_populates="payment")
