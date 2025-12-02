"""
Password hashing utilities for secure password storage.
"""
from passlib.context import CryptContext


# Create context for Argon2 hashing (no character limit)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using Argon2.
    
    Args:
        password: Plain-text password
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a hashed password using Argon2.
    
    Args:
        plain_password: Plain-text password
        hashed_password: Hashed password to verify against
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)
