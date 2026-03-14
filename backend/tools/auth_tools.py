
"""
Authentication Tools
Helper functions for user authentication
"""

def check_password_strength(password: str) -> dict:
    """
    Check if password meets security requirements
    
    Args:
        password: Password to check
        
    Returns:
        dict with 'valid' bool and 'message' str
    """
    if len(password) < 6:
        return {
            "valid": False,
            "message": "Password must be at least 6 characters long"
        }
    
    if not any(char.isupper() for char in password):
        return {
            "valid": False,
            "message": "Password must contain at least one uppercase letter"
        }
    
    if not any(char.isdigit() for char in password):
        return {
            "valid": False,
            "message": "Password must contain at least one digit"
        }
    
    return {
        "valid": True,
        "message": "Password is strong"
    }


def validate_email(email: str) -> dict:
    """
    Validate email format
    
    Args:
        email: Email to validate
        
    Returns:
        dict with 'valid' bool and 'message' str
    """
    if "@" not in email:
        return {
            "valid": False,
            "message": "Invalid email format"
        }
    
    parts = email.split("@")
    if len(parts) != 2:
        return {
            "valid": False,
            "message": "Invalid email format"
        }
    
    local, domain = parts
    if not local or not domain:
        return {
            "valid": False,
            "message": "Invalid email format"
        }
    
    if "." not in domain:
        return {
            "valid": False,
            "message": "Invalid email domain"
        }
    
    return {
        "valid": True,
        "message": "Email is valid"
    }


def validate_user_data(email: str, password: str, full_name: str) -> dict:
    """
    Validate all user data together
    
    Args:
        email: User email
        password: User password
        full_name: User full name
        
    Returns:
        dict with 'valid' bool and 'errors' list
    """
    errors = []
    
    # Validate email
    email_check = validate_email(email)
    if not email_check["valid"]:
        errors.append(email_check["message"])
    
    # Validate password
    password_check = check_password_strength(password)
    if not password_check["valid"]:
        errors.append(password_check["message"])
    
    # Validate name
    if len(full_name) < 2:
        errors.append("Full name must be at least 2 characters")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
