"""
Security utilities for authentication and authorization
Handles JWT token generation and verification
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
import os
from jwt import PyJWTError
import logging

logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Dictionary containing user data (e.g., user_id, email)
        expires_delta: Custom expiration time (default: 7 days)
    
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": "access"})
    
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating access token: {str(e)}")
        raise


def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT refresh token
    
    Args:
        data: Dictionary containing user data (e.g., user_id, email)
        expires_delta: Custom expiration time (default: 30 days)
    
    Returns:
        Encoded JWT refresh token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=30)  # Refresh tokens last longer
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": "refresh"})
    
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating refresh token: {str(e)}")
        raise


def get_password_hash(password: str) -> str:
    """
    Alias for hash_password to match common naming conventions
    """
    return hash_password(password)


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode a JWT token
    
    Args:
        token: JWT token string to verify
    
    Returns:
        Decoded token data if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Token decoded successfully. Payload keys: {list(payload.keys())}")
        return payload
    except PyJWTError as e:
        logger.error(f"Token verification failed: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error verifying token: {str(e)}")
        return None


def get_user_id_from_token(token: str) -> Optional[int]:
    """
    Extract user ID from JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        User ID if token is valid, None otherwise
    """
    payload = verify_token(token)
    if payload:
        return payload.get("user_id")
    return None


def hash_password(password: str) -> str:
    """
    Hash a password using Django's password hashing
    
    Args:
        password: Plain text password
    
    Returns:
        Hashed password string
    """
    from django.contrib.auth.hashers import make_password
    return make_password(password)


def check_password(password: str, hashed: str) -> bool:
    """
    Verify a password against a hash
    
    Args:
        password: Plain text password
        hashed: Hashed password string
    
    Returns:
        True if password matches, False otherwise
    """
    from django.contrib.auth.hashers import check_password as django_check_password
    return django_check_password(password, hashed)


def extract_token_from_header(authorization: str) -> Optional[str]:
    """
    Extract JWT token from Authorization header
    
    Args:
        authorization: Authorization header value (e.g., "Bearer <token>")
    
    Returns:
        JWT token string or None
    """
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
        return token
    except ValueError:
        return None
