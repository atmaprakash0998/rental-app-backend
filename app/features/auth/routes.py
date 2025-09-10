from fastapi import APIRouter, Depends, status, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from ...core.db import get_db_session
from ...core.middleware import get_current_user
from .controller import (
    register_user, login_user
)
from .schemas import UserLogin, UserRegister, UserOut, Token
from ...constants.permissions import Role

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
security = HTTPBearer()


async def get_current_user_dependency(request: Request) -> UserOut:
    """Dependency to get current authenticated user from middleware"""
    return await get_current_user(request)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db_session)
):
    """Register a new user"""
    return await register_user(db, user_data)


# @router.post("/login", response_model=Token)
# async def login(
#     login_data: UserLogin,
#     db: Session = Depends(get_db_session)
# ):
#     """Login user and get access token"""
#     return await login_user(db, login_data, Role.USER)

    

@router.post("/owner/login", response_model=Token)
async def owner_login(
    login_data: UserLogin,
    db: Session = Depends(get_db_session)
):
    """Login user and get access token"""
    return await login_user(db, login_data, Role.OWNER)