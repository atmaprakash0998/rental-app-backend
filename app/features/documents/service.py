import base64
import os
import uuid
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models.document import Document
from ..models.media_document import MediaDocument
from ..models.media_document_url import MediaDocumentUrl
from .schemas import DocumentData


# Module-level config for uploads directory
UPLOAD_DIR = "uploads/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_base64_image(base64_string: str, document_type: str, document_number: str) -> str:
    """
    Save base64 image to file system and return file path
    """
    try:
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]

        image_data = base64.b64decode(base64_string)

        file_extension = "jpg"
        filename = f"{document_type}_{document_number}_{uuid.uuid4().hex}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, 'wb') as f:
            f.write(image_data)

        return file_path
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to save image: {str(e)}"
        )


async def create_document_with_media(
    db: Session,
    document_data: DocumentData,
    entity_type: str,
    entity_id: uuid.UUID,
    added_by: str
) -> Document:
    """
    Create a document with its associated media
    """
    try:
        file_path = await save_base64_image(
            document_data.document_image,
            document_data.document_type,
            document_data.document_number
        )

        media_url = MediaDocumentUrl(
            type='image',
            url=file_path,
            encoding='base64',
            added_by=added_by
        )
        db.add(media_url)
        db.flush()

        document = Document(
            type=document_data.document_type,
            entity_type=entity_type,
            entity_id=entity_id,
            document_number=document_data.document_number,
            expiry_date=document_data.expiry_date,
            issue_date=document_data.issue_date,
            verification_status='pending',
            added_by=added_by
        )
        db.add(document)
        db.flush()

        media_document = MediaDocument(
            documents_id=document.id,
            media_documents_urls_id=media_url.id,
            added_by=added_by
        )
        db.add(media_document)
        db.flush()

        return document
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create document: {str(e)}"
        )


async def create_multiple_documents(
    db: Session,
    documents_data: List[DocumentData],
    entity_type: str,
    entity_id: uuid.UUID,
    added_by: str
) -> List[Document]:
    """
    Create multiple documents for an entity
    """
    try:
        created_documents = []
        for doc_data in documents_data:
            document = await create_document_with_media(
                db, doc_data, entity_type, entity_id, added_by
            )
            created_documents.append(document)

        db.commit()
        return created_documents
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create documents: {str(e)}"
        )


async def update_documents_for_entity(
    db: Session,
    entity_type: str,
    entity_id: uuid.UUID,
    documents_data: List[DocumentData],
    modified_by: str
) -> List[Document]:
    """
    Update documents for an entity (soft delete existing and create new ones)
    """
    try:
        existing_docs = db.query(Document).filter(
            Document.entity_type == entity_type,
            Document.entity_id == entity_id,
            Document.is_deleted == False
        ).all()

        for doc in existing_docs:
            doc.is_deleted = True
            doc.modified_date = datetime.utcnow()
            doc.modified_by = modified_by

            for media_doc in doc.media_documents:
                media_doc.is_deleted = True
                media_doc.modified_by = modified_by

        new_documents = await create_multiple_documents(
            db, documents_data, entity_type, entity_id, modified_by
        )

        return new_documents
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update documents: {str(e)}"
        )


async def get_documents_for_entity(
    db: Session,
    entity_type: str,
    entity_id: uuid.UUID
) -> List[Document]:
    """
    Get all active documents for an entity
    """
    try:
        return db.query(Document).filter(
            Document.entity_type == entity_type,
            Document.entity_id == entity_id,
            Document.is_deleted == False
        ).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get documents: {str(e)}"
        )
