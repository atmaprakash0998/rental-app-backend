from enum import Enum
from typing import List, Set
from functools import wraps
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from ..features.auth.schemas import UserOut


class Permission(str, Enum):
    """Define all available permissions in the system"""
    # User permissions
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    
    # Vehicle permissions
    VEHICLE_READ = "vehicle:read"
    VEHICLE_CREATE = "vehicle:create"
    VEHICLE_UPDATE = "vehicle:update"
    VEHICLE_DELETE = "vehicle:delete"
    
    # Booking permissions
    BOOKING_READ = "booking:read"
    BOOKING_CREATE = "booking:create"
    BOOKING_UPDATE = "booking:update"
    BOOKING_DELETE = "booking:delete"
    
    # Payment permissions
    PAYMENT_READ = "payment:read"
    PAYMENT_CREATE = "payment:create"
    PAYMENT_UPDATE = "payment:update"
    
    # Admin permissions
    ADMIN_READ = "admin:read"
    ADMIN_CREATE = "admin:create"
    ADMIN_UPDATE = "admin:update"
    ADMIN_DELETE = "admin:delete"
    
    # Owner permissions
    OWNER_READ = "owner:read"
    OWNER_UPDATE = "owner:update"


class Role(str, Enum):
    """Define user roles"""
    USER = "user"
    OWNER = "owner"
    ADMIN = "admin"


class EntityType(str, Enum):
    """Define user roles"""
    USER = "user"
    VEHICLE = "vehicle"

class Status(str, Enum):
    """Define user roles"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    REJECTED = "rejected"
    APPROVED = "approved"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    
# Role-based permissions mapping
ROLE_PERMISSIONS: dict[Role, Set[Permission]] = {
    Role.USER: {
        Permission.USER_READ,
        Permission.USER_UPDATE,
        Permission.VEHICLE_READ,
        Permission.BOOKING_READ,
        Permission.BOOKING_CREATE,
        Permission.BOOKING_UPDATE,
        Permission.PAYMENT_READ,
        Permission.PAYMENT_CREATE,
    },
    
    Role.OWNER: {
        Permission.USER_READ,
        Permission.USER_UPDATE,
        Permission.VEHICLE_READ,
        Permission.VEHICLE_CREATE,
        Permission.VEHICLE_UPDATE,
        Permission.VEHICLE_DELETE,
        Permission.BOOKING_READ,
        Permission.BOOKING_CREATE,
        Permission.BOOKING_UPDATE,
        Permission.BOOKING_DELETE,
        Permission.PAYMENT_READ,
        Permission.PAYMENT_CREATE,
        Permission.PAYMENT_UPDATE,
    },
    
    Role.ADMIN: {
        # Admin has all permissions
        Permission.USER_READ,
        Permission.USER_UPDATE,
        Permission.USER_DELETE,
        Permission.VEHICLE_READ,
        Permission.VEHICLE_CREATE,
        Permission.VEHICLE_UPDATE,
        Permission.VEHICLE_DELETE,
        Permission.BOOKING_READ,
        Permission.BOOKING_CREATE,
        Permission.BOOKING_UPDATE,
        Permission.BOOKING_DELETE,
        Permission.PAYMENT_READ,
        Permission.PAYMENT_CREATE,
        Permission.PAYMENT_UPDATE,
        Permission.ADMIN_READ,
        Permission.ADMIN_CREATE,
        Permission.ADMIN_UPDATE,
        Permission.ADMIN_DELETE,
        Permission.OWNER_READ,
        Permission.OWNER_UPDATE,
    }
}


def get_user_permissions(user_role: str) -> Set[Permission]:
    """Get permissions for a given user role"""
    try:
        role = Role(user_role)
        return ROLE_PERMISSIONS.get(role, set())
    except ValueError:
        # Invalid role
        return set()


def has_permission(user_role: str, required_permission: Permission) -> bool:
    """Check if user role has the required permission"""
    try:
        user_permissions = get_user_permissions(user_role)
        return required_permission in user_permissions
    except Exception:
        return False


def require_permission(permission: Permission):
    """Decorator to require specific permission for a route"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current_user from kwargs
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            if not has_permission(current_user.type, permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions. Required: {permission.value}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_role(allowed_roles: List[Role]):
    """Decorator to require specific roles for a route"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current_user from kwargs
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            try:
                user_role = Role(current_user.type)
                if user_role not in allowed_roles:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Access denied. Required roles: {[role.value for role in allowed_roles]}"
                    )
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid user role"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# Dependency functions for FastAPI
async def require_permission_dependency(
    permission: Permission,
    current_user: UserOut = Depends(lambda: None)  # This will be injected by the route
) -> UserOut:
    """FastAPI dependency to check permissions"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    if not has_permission(current_user.type, permission):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions. Required: {permission.value}"
        )
    
    return current_user


async def require_role_dependency(
    allowed_roles: List[Role],
    current_user: UserOut = Depends(lambda: None)  # This will be injected by the route
) -> UserOut:
    """FastAPI dependency to check roles"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    try:
        user_role = Role(current_user.type)
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[role.value for role in allowed_roles]}"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid user role"
        )
    
    return current_user


# Convenience functions for common role checks
def require_admin():
    """Require admin role"""
    return require_role([Role.ADMIN])


def require_owner_or_admin():
    """Require owner or admin role"""
    return require_role([Role.OWNER, Role.ADMIN])


def require_user_or_above():
    """Require user role or above (any authenticated user)"""
    return require_role([Role.USER, Role.OWNER, Role.ADMIN])
