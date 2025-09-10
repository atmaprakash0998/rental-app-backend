from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
import uuid


class DocumentData(BaseModel):
    document_number: Optional[str] = Field(default=None, description="Document number like AZAAP23432")
    document_image: str = Field(..., description="Base64 encoded document image")
    document_type: str = Field(..., description="Type of document")
    expiry_date: Optional[str] = Field(default=None, description="Expiry date of the document")
    issue_date: Optional[str] = Field(default=None, description="Issue date of the document")


class VehicleCreate(BaseModel):
    name: str = Field(..., description="Name of the vehicle")
    type: str = Field(pattern="^(bike|car|scooter|scooty|van)$")
    availability_status: str = Field(pattern="^(available|booked|maintenance)$")
    rental_duration: str = Field(pattern="^(hour|day|week|month)$")
    rental_price: Optional[float] = None
    documents: List[DocumentData] = Field(..., description="List of documents required for vehicle registration")


class VehicleUpdate(BaseModel):
    name: str = Field(..., description="Name of the vehicle")
    type: str = Field(..., pattern="^(bike|car|scooter|scooty|van)$")
    rental_duration: str = Field(..., pattern="^(hour|day|week|month)$")
    rental_price: float = Field(..., description="Rental price of the vehicle")
    availability_status: str = Field(..., pattern="^(available|booked|maintenance)$")
    documents: Optional[List[DocumentData]] = Field(default=None, description="List of documents to update for vehicle")


class VehicleOut(BaseModel):
    id: uuid.UUID
    name: str
    type: str
    availability_status: str
    rental_duration: str
    rental_price: Optional[float]
    is_deleted: bool
    model_config = {
        "from_attributes": True,
    }


class VehicleOwnerOut(BaseModel):
    """Schema for vehicle data returned by get_vehicle_by_owner_id"""
    user_vehicle_id: int
    ownership_type: str
    vehicle_id: uuid.UUID
    vehicle_name: str
    vehicle_type: str
    rental_duration: str
    rental_price: Optional[float]
    availability_status: str
    model_config = {
        "from_attributes": True,
    }


