from typing import Dict, Any, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends

from ...core.db import get_db_session
from .service import get_settings_by_keys, get_all_settings


async def get_settings_by_keys_controller(
    keys: List[str],
    db: Session = Depends(get_db_session)
) -> List[Dict[str, Any]]:
    """
    Get multiple settings by keys - returns only key and value
    """
    try:
        if not keys:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one key is required"
            )
        
        results = await get_settings_by_keys(db, keys)
        return [
            {"key": setting_key, "value": setting_value}
            for setting_key, setting_value in results
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get settings: {str(e)}"
        )


async def get_all_settings_controller(
    db: Session = Depends(get_db_session)
) -> List[Dict[str, Any]]:
    """
    Get all settings - returns only key and value
    """
    try:
        settings = await get_all_settings(db)
        return [
            {"key": setting_key, "value": setting_value}
            for setting_key, setting_value in settings
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get settings: {str(e)}"
        )
