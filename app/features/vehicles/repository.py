from datetime import datetime
from typing import List, Optional

from ...constants.permissions import EntityType, Role, Status
from ..documents.service import create_multiple_documents, update_documents_for_entity
from sqlalchemy.orm import Session
import uuid

from ..models.vehicle import Vehicle
from ..models.user_vehicle import UserVehicle
from .schemas import VehicleCreate, VehicleUpdate


async def list_vehicles(db: Session) -> List[Vehicle]:
    try:
        return db.query(Vehicle).filter(Vehicle.is_deleted == False).all()
    except Exception as e:
        raise Exception(f"Failed to list vehicles: {str(e)}")


async def create_vehicle(db: Session, owner_id: uuid.UUID, data: VehicleCreate) -> Vehicle:
    try:
        vehicle = Vehicle(
            name=data.name,
            type=data.type,
            rental_duration=data.rental_duration,
            rental_price=data.rental_price,
            availability_status=data.availability_status,
            added_by=str(owner_id)
        )
        db.add(vehicle)
        db.flush()

        linkVehicleOwner = UserVehicle(
            user_id=owner_id,
            vehicle_id=vehicle.id,
            ownership_type=Role.OWNER,
            ownership_status=Status.ACTIVE,
            ownership_start_date=datetime.utcnow(),
        )
        db.add(linkVehicleOwner)
        
        # Create documents for the vehicle
        if data.documents:
            await create_multiple_documents(
                db=db,
                documents_data=data.documents,
                entity_type=EntityType.VEHICLE,
                entity_id=vehicle.id,
                added_by=str(owner_id)
            )
        
        db.commit()
        db.refresh(vehicle)
        return vehicle
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to create vehicle: {str(e)}")


async def get_vehicle_by_id(db: Session, vehicle_id: uuid.UUID) -> Optional[Vehicle]:
    try:
        return db.query(Vehicle).filter(Vehicle.id == vehicle_id, Vehicle.is_deleted == False).first()
    except Exception as e:
        raise Exception(f"Failed to get vehicle: {str(e)}")


async def is_owner_of_vehicle(db: Session, owner_id: uuid.UUID, vehicle_id: uuid.UUID) -> bool:
    try:
        link = db.query(UserVehicle).filter(
            UserVehicle.user_id == owner_id,
            UserVehicle.vehicle_id == vehicle_id,
            UserVehicle.ownership_type == 'owner',
            UserVehicle.ownership_status == 'active',
            UserVehicle.is_deleted == False,
        ).first()
        return link is not None
    except Exception as e:
        raise Exception(f"Failed to verify ownership: {str(e)}")


async def update_vehicle(db: Session, owner_id: uuid.UUID, vehicle_id: uuid.UUID, data: VehicleUpdate) -> Vehicle:
    try:
        vehicle = await get_vehicle_by_id(db, vehicle_id)
        if vehicle is None:
            raise Exception("Vehicle not found")

        if not await is_owner_of_vehicle(db, owner_id, vehicle_id):
            raise Exception("Not authorized to update this vehicle")
        if data.name is not None:
            vehicle.name = data.name
        if data.type is not None:
            vehicle.type = data.type
        if data.rental_duration is not None:
            vehicle.rental_duration = data.rental_duration
        if data.rental_price is not None:
            vehicle.rental_price = data.rental_price
        if data.availability_status is not None:
            vehicle.availability_status = data.availability_status

        # Update documents if provided
        if data.documents is not None:
            await update_documents_for_entity(
                db=db,
                entity_type=EntityType.VEHICLE,
                entity_id=vehicle_id,
                documents_data=data.documents,
                modified_by=str(owner_id)
            )

        vehicle.modified_date = datetime.utcnow()
        vehicle.modified_by = str(owner_id)
        db.commit()
        db.refresh(vehicle)
        return vehicle
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to update vehicle: {str(e)}")


async def delete_vehicle(db: Session, owner_id: uuid.UUID, vehicle_id: uuid.UUID) -> None:
    try:
        vehicle = await get_vehicle_by_id(db, vehicle_id)
        if vehicle is None:
            raise Exception("Vehicle not found")

        if not await is_owner_of_vehicle(db, owner_id, vehicle_id):
            raise Exception("Not authorized to delete this vehicle")

        vehicle.is_deleted = True
        vehicle.modified_date = datetime.utcnow()
        vehicle.modified_by = str(owner_id)

        # soft-delete ownership row as well
        db.query(UserVehicle).filter(
            UserVehicle.user_id == owner_id,
            UserVehicle.vehicle_id == vehicle_id,
            UserVehicle.ownership_type == 'owner',
        ).update({UserVehicle.is_deleted: True})

        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to delete vehicle: {str(e)}")



# Write a function to get specific fields from both user_vehicles and vehicles tables
async def get_vehicle_by_owner_id(db: Session, owner_id: uuid.UUID) -> List[dict]:
    try:
        results = db.query(
            # Fields from UserVehicle table
            UserVehicle.id,
            UserVehicle.ownership_type,
            # Fields from Vehicle table
            Vehicle.id.label('vehicle_id'),
            Vehicle.name,
            Vehicle.type,
            Vehicle.rental_duration,
            Vehicle.rental_price,
            Vehicle.availability_status,
        ).join(
            Vehicle,
            UserVehicle.vehicle_id == Vehicle.id
        ).filter(
            UserVehicle.user_id == owner_id,
            UserVehicle.ownership_type == 'owner',
            UserVehicle.ownership_status == 'active',
            UserVehicle.is_deleted == False,
            Vehicle.is_deleted == False
        ).all()
        
        return [
            {
                # UserVehicle fields
                "user_vehicle_id": id,
                "ownership_type": ownership_type,
                # Vehicle fields
                "vehicle_id": vehicle_id,
                "vehicle_name": name,
                "vehicle_type": type,
                "rental_duration": rental_duration,
                "rental_price": rental_price,
                "availability_status": availability_status,
            }
            for id, ownership_type, vehicle_id, name, type, rental_duration, rental_price, availability_status in results
        ]
    except Exception as e:
        raise Exception(f"Failed to get vehicles by owner id: {str(e)}")