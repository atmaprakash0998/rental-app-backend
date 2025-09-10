from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Boolean, DateTime, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from ...core.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    type: Mapped[str] = mapped_column(Enum('user', 'owner', 'admin', name='user_type'), nullable=False)
    sub_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(10), nullable=False)
    password: Mapped[Optional[str]] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(Enum('active', 'inactive', 'pending', name='user_status'), default='active')
    additional_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    added_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    modified_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=datetime.utcnow)
    added_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    modified_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    user_vehicles: Mapped[List["UserVehicle"]] = relationship("UserVehicle", back_populates="user")
