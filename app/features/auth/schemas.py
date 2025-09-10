from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field
import uuid


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
    name: str = Field(min_length=3, max_length=100)
    phone: Optional[str] = Field(default=None, min_length=10, max_length=10)
    type: str = Field(default="user", pattern="^(user|owner|admin)$")


class UserOut(BaseModel):
    id: uuid.UUID
    type: str
    sub_type: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    status: str
    additional_data: Optional[Dict[str, Any]] = None
    is_deleted: bool
    added_date: datetime
    modified_date: Optional[datetime] = None
    added_by: Optional[str] = None
    modified_by: Optional[str] = None

    model_config = {
        "from_attributes": True,
    }


class Token(BaseModel):
    access_token: str
    user_data: dict = {
        "name": str,
        "email": str,
        "phone": str
    }


class TokenData(BaseModel):
    email: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    phone: Optional[str] = Field(default=None, min_length=10, max_length=10)
    sub_type: Optional[str] = Field(default=None, max_length=100)
    additional_data: Optional[Dict[str, Any]] = None


class PasswordChange(BaseModel):
    current_password: str = Field(min_length=6, max_length=100)
    new_password: str = Field(min_length=6, max_length=100)
