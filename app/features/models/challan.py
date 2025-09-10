from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, Enum, Numeric, JSON, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from ...core.db import Base


class Challan(Base):
    __tablename__ = "challans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    entity_type: Mapped[str] = mapped_column(Enum('user', 'vehicle', name='challan_entity_type'), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
    challan_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    authority_name: Mapped[str] = mapped_column(Enum('police', 'traffic', 'other', name='authority_name'), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    amount: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    additional_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(Enum('pending', 'paid', name='challan_status'), default='pending')
    added_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    modified_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=datetime.utcnow)
    added_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    modified_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
