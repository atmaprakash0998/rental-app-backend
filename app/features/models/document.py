from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, Enum, JSON, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ...core.db import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    sub_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    entity_type: Mapped[str] = mapped_column(Enum('user', 'vehicle', name='entity_type'), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    document_number: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    expiry_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    issue_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    verification_status: Mapped[str] = mapped_column(Enum('pending', 'verified', 'rejected', name='verification_status'), default='pending')
    additional_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    added_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    modified_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=datetime.utcnow)
    added_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    modified_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    media_documents: Mapped[list["MediaDocument"]] = relationship("MediaDocument", back_populates="document")
