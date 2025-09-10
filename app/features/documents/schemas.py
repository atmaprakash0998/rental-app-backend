from ast import pattern
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class DocumentData(BaseModel):
    document_number: Optional[str] = Field(default=None, description="Document number like AZAAP23432")
    document_image: str = Field(..., description="Base64 encoded document image")
    document_type: str = Field(..., description="Type of document")
    expiry_date: Optional[datetime] = Field(default=None, pattern="^[0-9]{2}/[0-9]{2}/[0-9]{4}$", description="Document expiry date")
    issue_date: Optional[datetime] = Field(default=None, pattern="^[0-9]{2}/[0-9]{2}/[0-9]{4}$", description="Document issue date")


class DocumentOut(BaseModel):
    id: int
    type: str
    document_number: Optional[str]
    expiry_date: Optional[datetime]
    issue_date: Optional[datetime]
    verification_status: str
    added_date: datetime
    modified_date: Optional[datetime]
    
    model_config = {
        "from_attributes": True,
    }


class MediaDocumentUrlOut(BaseModel):
    id: int
    type: str
    file_path: Optional[str]
    encoding: Optional[str]
    
    model_config = {
        "from_attributes": True,
    }


class DocumentWithMediaOut(BaseModel):
    id: int
    type: str
    document_number: Optional[str]
    verification_status: str
    added_date: datetime
    media_documents: List[MediaDocumentUrlOut]
    
    model_config = {
        "from_attributes": True,
    }
