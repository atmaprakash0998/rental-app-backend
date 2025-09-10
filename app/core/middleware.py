from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
from typing import Optional

from .db import SessionLocal
from ..features.auth.repository import verify_token, get_user_by_id
from ..features.auth.schemas import UserOut


# Default excluded paths for authentication
DEFAULT_EXCLUDED_PATHS = [
    "/api/v1/auth/register",
    "/api/v1/auth/login", 
    "/api/v1/auth/owner/login",
    "/api/v1/greeting",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/health",
]


def is_path_excluded(request_path: str, excluded_paths: list) -> bool:
    """Check if the request path should be excluded from authentication"""
    try:
        print("request_path", request_path)
        print("excluded_paths", excluded_paths)
        print("any(request_path == path for path in excluded_paths)", any(request_path == path for path in excluded_paths))
        return any(request_path == path for path in excluded_paths)
    except Exception:
        return False


def extract_authorization_token(request: Request) -> Optional[str]:
    """Extract Bearer token from Authorization header"""
    try:
        authorization = request.headers.get("Authorization")
        if not authorization:
            return None
        
        if not authorization.startswith("Bearer "):
            return None
            
        return authorization.split(" ")[1]
    except Exception:
        return None


async def validate_token_and_user_data(token: str) -> dict:
    """Validate JWT token and return user information"""
    db = SessionLocal()
    try:
        # Verify token and get payload
        payload = verify_token(token)
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Extract user_id and type from token payload
        user_id = payload.get("user_id")
        user_type = payload.get("type")
        
        if not user_id or not user_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Get user by ID (more efficient than searching by email)
        user = await get_user_by_id(db, uuid.UUID(user_id), user_type)
                
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "user_id": user.id,
            "user_type": user.type,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token validation failed",
            headers={"WWW-Authenticate": "Bearer"},
        )
    finally:
        db.close()


def set_user_in_request_state(request: Request, user_data: dict) -> None:
    """Set user information in request state"""
    try:
        request.state.user_id = user_data["user_id"]
        request.state.user_type = user_data["user_type"]
    except Exception as e:
        print(f"Error setting user state: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to set user state"
        )


async def auth_middleware_dispatch(request: Request, call_next, excluded_paths: list = None):
    """Functional middleware for authentication"""
    try:
        # Use default excluded paths if none provided
        excluded_paths = excluded_paths or DEFAULT_EXCLUDED_PATHS
        
        # Skip authentication for excluded paths
        if is_path_excluded(request.url.path, excluded_paths):
            response = await call_next(request)
            return response

        # Extract token from Authorization header
        token = extract_authorization_token(request)
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Validate token and get user
        user_data = await validate_token_and_user_data(token)
        
        # Set user information in request state
        set_user_in_request_state(request, user_data)

        # Continue to the next middleware/route
        response = await call_next(request)
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )


class AuthMiddleware(BaseHTTPMiddleware):
    """Wrapper class to make functional middleware compatible with FastAPI"""
    def __init__(self, app, excluded_paths: list = None):
        super().__init__(app)
        self.excluded_paths = excluded_paths

    async def dispatch(self, request: Request, call_next):
        return await auth_middleware_dispatch(request, call_next, self.excluded_paths)


async def get_current_user(request: Request) -> UserOut:
    """Get current authenticated user from request state"""
    try:
        # Check if user data is available in request state
        if not hasattr(request.state, 'user_id') or not hasattr(request.state, 'user_type'):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database
        db = SessionLocal()
        try:
            user = await get_user_by_id(db, request.state.user_id, request.state.user_type)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return UserOut(
                id=user.id,
                email=user.email,
                name=user.name,
                phone=user.phone,
                type=user.type,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        finally:
            db.close()
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to get current user",
            headers={"WWW-Authenticate": "Bearer"},
        )

