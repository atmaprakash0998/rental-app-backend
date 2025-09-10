from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, JSON, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...core.db import Base


class MediaDocument(Base):
    __tablename__ = "media_documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    documents_id: Mapped[int] = mapped_column(Integer, ForeignKey("documents.id"), nullable=False)
    media_documents_urls_id: Mapped[int] = mapped_column(Integer, ForeignKey("media_documents_urls.id"), nullable=False)
    additional_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    added_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    modified_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    document: Mapped["Document"] = relationship("Document", back_populates="media_documents")
    media_document_url: Mapped["MediaDocumentUrl"] = relationship("MediaDocumentUrl", back_populates="media_documents")
