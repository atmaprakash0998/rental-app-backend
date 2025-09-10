from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import uuid

from ...core.config import get_settings
from ..models.user import User
from .schemas import UserRegister, UserUpdate, PasswordChange

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Get settings
settings = get_settings()
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        # Log the error if needed
        raise Exception(f"Password verification failed: {str(e)}")


def get_password_hash(password: str) -> str:
    """Hash a password"""
    try:
        return pwd_context.hash(password)
    except Exception as e:
        raise Exception(f"Password hashing failed: {str(e)}")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token with user role and permissions"""
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        raise Exception(f"Token creation failed: {str(e)}")


async def get_user_by_email(db: Session, email: str, type: str) -> Optional[User]:
    """Get user by email"""
    try:
        return db.query(User).filter(User.email == email, User.is_deleted == False, User.status == 'active', User.type == type).first()
    except Exception as e:
        raise Exception(f"Failed to get user by email: {str(e)}")


async def get_user_by_id(db: Session, user_id: uuid.UUID, type: str) -> Optional[User]:
    """Get user by ID"""
    try:
        return db.query(User).filter(User.id == user_id, User.is_deleted == False, User.status == 'active', User.type == type).first()
    except Exception as e:
        raise Exception(f"Failed to get user by ID: {str(e)}")


async def create_user(db: Session, user_data: UserRegister) -> None:
    """Create a new user"""
    try:
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            password=hashed_password,
            name=user_data.name,
            phone=user_data.phone,
            type=user_data.type,
            sub_type=None,
            additional_data={},
            status='active'  # Default status for new users
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        # Rollback the transaction in case of error
        db.rollback()
        # Re-raise the exception so it can be handled by the controller
        raise e


async def authenticate_user(db: Session, email: str, password: str, type: str) -> Optional[User]:
    """Authenticate user with email and password"""
    try:
        user = await get_user_by_email(db, email, type)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user
    except Exception as e:
        raise Exception(f"User authentication failed: {str(e)}")


async def update_user(db: Session, user: User, user_data: UserUpdate) -> User:
    """Update user information"""
    try:
        if user_data.name is not None:
            user.name = user_data.name
        if user_data.phone is not None:
            user.phone = user_data.phone
        if user_data.sub_type is not None:
            user.sub_type = user_data.sub_type
        if user_data.additional_data is not None:
            user.additional_data = user_data.additional_data
        
        user.modified_date = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise Exception(f"User update failed: {str(e)}")


async def change_password(db: Session, user: User, password_data: PasswordChange) -> bool:
    """Change user password"""
    try:
        # Verify current password
        if not verify_password(password_data.current_password, user.password):
            return False
        
        # Update password
        user.password = get_password_hash(password_data.new_password)
        user.modified_date = datetime.utcnow()
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise Exception(f"Password change failed: {str(e)}")


def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return token payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        user_type: str = payload.get("type")
        
        if user_id is None or user_type is None:
            return None
            
        # Validate that user_id is a valid UUID
        try:
            uuid.UUID(user_id)
        except (ValueError, TypeError):
            # user_id is not a valid UUID
            return None
            
        return {
            "user_id": user_id,
            "type": user_type
        }
    except JWTError as e:
        # JWT errors are expected for invalid tokens
        return None
    except Exception as e:
        # Other unexpected errors
        raise Exception(f"Token verification failed: {str(e)}")
