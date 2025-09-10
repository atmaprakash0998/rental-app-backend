from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
import uuid

from ...core.db import get_db_session
from ...constants.permissions import Role
from ...utils.helpers import is_user_type_in_allowed_roles
from .service import get_documents_for_entity
from .schemas import DocumentOut

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.get("/vehicle/{vehicle_id}", response_model=list[DocumentOut])
async def get_vehicle_documents(
    vehicle_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db_session),
):
    """Get all documents for a specific vehicle"""
    try:     
        # Check if user has required role (Owner or Admin)
        if not is_user_type_in_allowed_roles(request.state.user_type, [Role.OWNER, Role.ADMIN]):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        documents = await get_documents_for_entity(db, "vehicle", vehicle_id)
        return [DocumentOut.model_validate(doc) for doc in documents]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get vehicle documents: {str(e)}"
        )
