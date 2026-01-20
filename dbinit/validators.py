"""Password validation utilities."""

import re
from typing import Dict


def validate_password_strength(password: str) -> Dict[str, any]:
    """Validate password strength.
    
    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)
    
    Args:
        password: Password to validate
        
    Returns:
        Dictionary with 'valid' (bool) and 'message' (str) keys
    """
    if len(password) < 8:
        return {
            "valid": False,
            "message": "Password must be at least 8 characters long"
        }
    
    if not re.search(r'[A-Z]', password):
        return {
            "valid": False,
            "message": "Password must contain at least one uppercase letter"
        }
    
    if not re.search(r'[a-z]', password):
        return {
            "valid": False,
            "message": "Password must contain at least one lowercase letter"
        }
    
    if not re.search(r'\d', password):
        return {
            "valid": False,
            "message": "Password must contain at least one digit"
        }
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        return {
            "valid": False,
            "message": "Password must contain at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)"
        }
    
    return {
        "valid": True,
        "message": "Password meets strength requirements"
    }
