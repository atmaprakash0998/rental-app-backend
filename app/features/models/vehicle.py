from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Boolean, DateTime, Enum, Numeric, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from ...core.db import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(Enum('bike', 'car', 'scooter', 'scooty', 'van', name='vehicle_type'), nullable=False)
    sub_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    availability_status: Mapped[str] = mapped_column(Enum('available', 'booked', 'maintenance', name='availability_status'), default='available')
    rental_duration: Mapped[str] = mapped_column(Enum('hour', 'day', 'week', 'month', name='rental_duration'), nullable=False)
    rental_price: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    additional_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    added_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    modified_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=datetime.utcnow)
    added_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    modified_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    user_vehicles: Mapped[List["UserVehicle"]] = relationship("UserVehicle", back_populates="vehicle")
