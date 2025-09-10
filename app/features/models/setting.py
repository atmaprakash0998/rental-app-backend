from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ...core.db import Base


class Setting(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    value: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    additional_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    added_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    modified_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=datetime.utcnow)
    added_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    modified_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
