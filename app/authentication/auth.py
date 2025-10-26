"""
Authentication utilities
"""
import os

def validate_credentials(username: str, password: str) -> bool:
    """ Validates user credentials.
    Parameter:
        username (str): Username to validate
        password (str): Password to validate
    Returns:
        bool: True if credentials are valid
    """
    admin_user = os.getenv("ADMIN_USERNAME", "admin")
    admin_pass = os.getenv("ADMIN_PASSWORD", "admin")
    return username == admin_user and password == admin_pass
