from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
import uuid

from ...core.db import get_db_session
from ...constants.permissions import Role
from ...utils.helpers import is_user_type_in_allowed_roles
from .schemas import VehicleCreate, VehicleUpdate, VehicleOut, VehicleOwnerOut
from .controller import (
    get_vehicles_by_owner_id,
    create_new_vehicle,
    edit_vehicle,
    remove_vehicle,
)

router = APIRouter(prefix="/api/v1/vehicles", tags=["vehicles"])

# Write a function to get the vehicles by owner id
@router.get("/get-owner-vehicles", response_model=list[VehicleOwnerOut])
async def owner_vehicles(
    Request: Request,
    db: Session = Depends(get_db_session),
):
    try:
        # Check if user has required role (Owner or Admin)
        if not is_user_type_in_allowed_roles(Request.state.user_type, [Role.OWNER, Role.ADMIN]):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        return await get_vehicles_by_owner_id(db, Request.state.user_id)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in owner_vehicles: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



@router.post("/create-vehicle", response_model=VehicleOut, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    Request: Request,
    payload: VehicleCreate,
    db: Session = Depends(get_db_session),
):
    try:
            
        # Check if user has required role (Owner or Admin)
        if not is_user_type_in_allowed_roles(Request.state.user_type, [Role.OWNER, Role.ADMIN]):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        return await create_new_vehicle(db, Request.state.user_id, payload)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/update-vehicle/{vehicle_id}", response_model=VehicleOut)
async def update_vehicle(
    vehicle_id: uuid.UUID,
    Request: Request,
    payload: VehicleUpdate,
    db: Session = Depends(get_db_session),
):
    try:
            
        # Check if user has required role (Owner or Admin)
        if not is_user_type_in_allowed_roles(Request.state.user_type, [Role.OWNER, Role.ADMIN]):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        return await edit_vehicle(db, Request.state.user_id, vehicle_id, payload)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/delete-vehicle/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(
    Request: Request,
    vehicle_id: uuid.UUID,
    db: Session = Depends(get_db_session),
):
    try:
            
        # Check if user has required role (Owner or Admin)
        if not is_user_type_in_allowed_roles(Request.state.user_type, [Role.OWNER, Role.ADMIN]):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        await remove_vehicle(db, Request.state.user_id, vehicle_id)
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
