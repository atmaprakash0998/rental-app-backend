from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, Enum, Numeric, JSON, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from ...core.db import Base


class UserVehicle(Base):
    __tablename__ = "user_vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    vehicle_id: Mapped[str] = mapped_column(String(36), ForeignKey("vehicles.id"), nullable=False)
    ownership_type: Mapped[str] = mapped_column(Enum('owner', 'renter', name='ownership_type'), default='owner')
    ownership_start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ownership_end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ownership_status: Mapped[str] = mapped_column(Enum('active', 'inactive', 'sold', name='ownership_status'), default='active')
    additional_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    total_price: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="user_vehicles")
    vehicle: Mapped["Vehicle"] = relationship("Vehicle", back_populates="user_vehicles")
