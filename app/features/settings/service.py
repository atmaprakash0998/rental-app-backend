from typing import Optional, Dict, Any, Tuple, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models.setting import Setting
from .schemas import SettingCreate, SettingUpdate


async def create_setting(
    db: Session,
    setting_data: SettingCreate,
    added_by: str
) -> Setting:
    """
    Create a new setting with dict value type
    """
    try:
        setting = Setting(
            key=setting_data.key,
            value=setting_data.value,  # This will be stored as JSON
            additional_data=setting_data.additional_data,
            added_by=added_by
        )
        db.add(setting)
        db.commit()
        db.refresh(setting)
        return setting
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create setting: {str(e)}"
        )

async def get_settings_by_keys(
    db: Session,
    keys: List[str]
) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Get multiple settings by their keys - returns only key and value columns
    """
    try:
        return db.query(Setting.key, Setting.value).filter(
            Setting.key.in_(keys),
            Setting.is_deleted == False
        ).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get settings: {str(e)}"
        )


async def update_setting(
    db: Session,
    setting_id: int,
    setting_data: SettingUpdate,
    modified_by: str
) -> Optional[Setting]:
    """
    Update an existing setting
    """
    try:
        setting = db.query(Setting).filter(
            Setting.id == setting_id,
            Setting.is_deleted == False
        ).first()
        
        if not setting:
            return None
            
        if setting_data.key is not None:
            setting.key = setting_data.key
        if setting_data.value is not None:
            setting.value = setting_data.value
        if setting_data.additional_data is not None:
            setting.additional_data = setting_data.additional_data
            
        setting.modified_by = modified_by
        db.commit()
        db.refresh(setting)
        return setting
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update setting: {str(e)}"
        )


async def get_all_settings(
    db: Session
) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Get all active settings - returns only key and value columns
    """
    try:
        return db.query(Setting.key, Setting.value).filter(
            Setting.is_deleted == False
        ).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get settings: {str(e)}"
        )


async def delete_setting(
    db: Session,
    setting_id: int,
    modified_by: str
) -> bool:
    """
    Soft delete a setting
    """
    try:
        setting = db.query(Setting).filter(
            Setting.id == setting_id,
            Setting.is_deleted == False
        ).first()
        
        if not setting:
            return False
            
        setting.is_deleted = True
        setting.modified_by = modified_by
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete setting: {str(e)}"
        )

