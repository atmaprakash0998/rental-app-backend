from typing import Optional, Union, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class SettingCreate(BaseModel):
    key: str = Field(..., description="Setting key identifier")
    value: dict = Field(..., description="Setting value")
    additional_data: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class SettingUpdate(BaseModel):
    key: Optional[str] = Field(default=None, description="Setting key identifier")
    value: Optional[Union[str, int, float, bool, List[Any], Dict[str, Any]]] = Field(default=None, description="Setting value")
    additional_data: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class SettingOut(BaseModel):
    id: int
    key: str
    value: Dict[str, Any]
    additional_data: Optional[Dict[str, Any]]
    is_deleted: bool
    added_date: datetime
    modified_date: Optional[datetime]
    added_by: Optional[str]
    modified_by: Optional[str]
    
    model_config = {
        "from_attributes": True,
    }
