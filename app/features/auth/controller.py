from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .repository import (
    get_user_by_email, create_user, authenticate_user, create_access_token
)
from .schemas import UserLogin, UserRegister, Token
from ...constants.permissions import Role, get_user_permissions


access_token_expire_minutes = 24 * 60 # 24 hours
 
async def register_user(db: Session, user_data: UserRegister) -> dict:
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = await get_user_by_email(db, user_data.email , Role.USER)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        await create_user(db, user_data)
        return {"message": "User registered successfully"}
        
    except HTTPException:
        # Re-raise HTTP exceptions (like email already exists)
        raise
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


async def login_user(db: Session, login_data: UserLogin, type: str) -> Token:
    """Authenticate user and return access token"""
    try:
        user = await authenticate_user(db, login_data.email, login_data.password, type)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user is active and not deleted
        if user.status != 'active':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User account is {user.status}. Please contact support."
            )
        
        if user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User account has been deleted"
            )
        
        # Create access token with user role and permissions
        access_token_expires = timedelta(minutes=access_token_expire_minutes)
        
        access_token = create_access_token(
            data={
                "user_id": str(user.id),
                "type": user.type,
            }, 
            expires_delta=access_token_expires
        )

        token_data = {
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
        }

        if(user.type != Role.USER):
            token_data["permissions"] = list(get_user_permissions(user.type))

        return Token(
            access_token= access_token,
            user_data= token_data
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

