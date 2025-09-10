from typing import Union, List
from ..constants.permissions import Role


def is_user_type_in_allowed_roles(user_type: str, allowed_roles: List[Union[str, Role]]) -> bool:
    """
    Check if the user_type is in the list of allowed roles.
    
    Args:
        user_type (str): The user type to check
        allowed_roles (List[Union[str, Role]]): List of allowed roles
        
    Returns:
        bool: True if user_type is in allowed_roles, False otherwise
    """
    try:
        # Convert user_type to Role enum for comparison
        user_role = Role(user_type)
        
        # Check if user_role is in any of the allowed roles
        for allowed_role in allowed_roles:
            # Convert string roles to Role enum if needed
            if isinstance(allowed_role, str):
                allowed_role = Role(allowed_role)
            
            if user_role == allowed_role:
                return True
        
        return False
    except ValueError:
        # If user_type is invalid, return False
        return False


def get_valid_user_types() -> List[str]:
    """
    Get a list of all valid user types.
    
    Returns:
        List[str]: List of all valid user type strings
    """
    return [role.value for role in Role]

