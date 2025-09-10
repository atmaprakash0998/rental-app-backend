from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, JSON, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...core.db import Base


class MediaDocumentUrl(Base):
    __tablename__ = "media_documents_urls"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[str] = mapped_column(Enum('image', name='media_type'), nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    file_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    encoding: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    additional_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    added_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    modified_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=datetime.utcnow)
    added_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    modified_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    media_documents: Mapped[list["MediaDocument"]] = relationship("MediaDocument", back_populates="media_document_url")
