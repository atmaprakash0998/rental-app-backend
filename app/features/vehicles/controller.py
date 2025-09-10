from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import uuid

from .schemas import VehicleCreate, VehicleUpdate, VehicleOut, VehicleOwnerOut
from .repository import (
    get_vehicle_by_owner_id,
    list_vehicles as repo_list_vehicles,
    create_vehicle,
    update_vehicle,
    delete_vehicle as repo_delete_vehicle,
)


async def list_all_vehicles(db: Session) -> List[VehicleOut]:
    try:
        vehicles = await repo_list_vehicles(db)
        return [VehicleOut.model_validate(v) for v in vehicles]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list vehicles: {str(e)}",
        )

# Write a function to get the vehicles by owner id
async def get_vehicles_by_owner_id(db: Session, owner_id: uuid.UUID) -> List[VehicleOwnerOut]:
    try:
        vehicles = await get_vehicle_by_owner_id(db, owner_id)
        result = [VehicleOwnerOut.model_validate(v) for v in vehicles]
        return result
    except Exception as e:
        print(f"Error in get_vehicles_by_owner_id: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get vehicles by owner id: {str(e)}",
        )


async def create_new_vehicle(db: Session, owner_id: uuid.UUID, data: VehicleCreate) -> VehicleOut:
    try:
        vehicle = await create_vehicle(db, owner_id, data)
        return VehicleOut.model_validate(vehicle)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create vehicle: {str(e)}",
        )

async def edit_vehicle(db: Session, owner_id: uuid.UUID, vehicle_id: uuid.UUID, data: VehicleUpdate) -> VehicleOut:
    try:
        vehicle = await update_vehicle(db, owner_id, vehicle_id, data)
        return VehicleOut.model_validate(vehicle)
    except Exception as e:
        status_code = status.HTTP_400_BAD_REQUEST if "Not authorized" in str(e) else status.HTTP_404_NOT_FOUND if "not found" in str(e).lower() else status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=status_code, detail=str(e))


async def remove_vehicle(db: Session, owner_id: uuid.UUID, vehicle_id: uuid.UUID) -> dict:
    try:
        await repo_delete_vehicle(db, owner_id, vehicle_id)
        return {"message": "Vehicle deleted successfully"}
    except Exception as e:
        status_code = status.HTTP_400_BAD_REQUEST if "Not authorized" in str(e) else status.HTTP_404_NOT_FOUND if "not found" in str(e).lower() else status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=status_code, detail=str(e))


