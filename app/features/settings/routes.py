from typing import Dict, Any, List
from fastapi import APIRouter, Request, HTTPException, Query

from .controller import (
    get_settings_by_keys_controller,
    get_all_settings_controller
)
from ...constants.permissions import Role
from ...utils.helpers import is_user_type_in_allowed_roles

router = APIRouter(prefix="/api/v1/settings", tags=["settings"])


#Inside the keys were passed as query params
#Example: /api/v1/settings/keys?keys=key1&keys=key2
@router.get("/keys", response_model=List[Dict[str, Any]])
async def get_settings_by_keys(
    request: Request,
    keys: List[str] = Query(..., description="List of setting keys to fetch")
):
    """
    Get multiple settings by keys - returns only key and value
    """
    # Validate the keys list is not empty
    if not keys:
        raise HTTPException(status_code=400, detail="At least one key is required")

    # Validate the role is owner or Admin
    if not is_user_type_in_allowed_roles(request.state.user_type, [Role.OWNER, Role.ADMIN]):
        raise HTTPException(status_code=403, detail="You are not authorized to access this resource")

    return await get_settings_by_keys_controller(keys)


@router.get("/", response_model=List[Dict[str, Any]])
async def get_all_settings():
    """
    Get all settings - returns only key and value
    """
    return await get_all_settings_controller()
