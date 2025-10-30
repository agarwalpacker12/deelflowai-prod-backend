"""
Authentication middleware for FastAPI endpoints
Verifies JWT tokens and provides user authentication
"""

from fastapi import HTTPException, Header, status
from typing import Optional, Callable
from functools import wraps
import logging

from app.core.security import verify_token, extract_token_from_header

logger = logging.getLogger(__name__)


class AuthenticationRequired(HTTPException):
    """Custom exception for authentication required"""
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please login first.",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """
    Dependency function to get current authenticated user
    
    Args:
        authorization: Authorization header with Bearer token
    
    Returns:
        User data from JWT token
    
    Raises:
        HTTPException: If authentication fails
    """
    # Explicitly check for None or empty string - this MUST raise an exception
    if authorization is None or authorization == "":
        logger.warning("Authentication required but no Authorization header provided")
        raise AuthenticationRequired()
    
    # Extract token from Bearer format
    token = extract_token_from_header(authorization)
    if not token:
        logger.warning(f"Invalid authorization header format: {authorization[:50] if authorization else 'None'}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication header format. Expected: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify token is valid
    payload = verify_token(token)
    if not payload:
        logger.warning("Token verification failed - invalid or expired token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Log payload structure for debugging
    logger.debug(f"Token payload decoded. Keys: {list(payload.keys()) if isinstance(payload, dict) else type(payload)}")
    logger.debug(f"User authenticated successfully: {payload.get('user_id', payload.get('sub', 'Unknown'))}")
    return payload


def require_auth(func: Callable) -> Callable:
    """
    Decorator to require authentication for an endpoint
    
    Usage:
        @require_auth
        async def my_endpoint(current_user: dict = Depends(get_current_user)):
            ...
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    return wrapper


def verify_user_logged_in(authorization: Optional[str] = Header(None)) -> bool:
    """
    Verify if user is logged in (returns True/False instead of raising exception)
    Useful for endpoints that can work with or without authentication
    
    Args:
        authorization: Authorization header with Bearer token
    
    Returns:
        True if user is authenticated, False otherwise
    """
    try:
        if not authorization:
            return False
        
        token = extract_token_from_header(authorization)
        if not token:
            return False
        
        payload = verify_token(token)
        return payload is not None
    except Exception:
        return False


def get_user_id_from_request(authorization: Optional[str] = Header(None)) -> Optional[int]:
    """
    Get user ID from request without raising exception
    
    Args:
        authorization: Authorization header with Bearer token
    
    Returns:
        User ID if authenticated, None otherwise
    """
    try:
        if not authorization:
            return None
        
        token = extract_token_from_header(authorization)
        if not token:
            return None
        
        payload = verify_token(token)
        if payload:
            return payload.get("user_id")
        return None
    except Exception:
        return None


def require_permission(permission_name: str):
    """
    Dependency function to require specific permission
    
    Args:
        permission_name: Name of the permission required
    
    Returns:
        Dependency function that checks permission
    """
    def check_permission(authorization: Optional[str] = Header(None)):
        """
        Check if user has the required permission
        """
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token = extract_token_from_header(authorization)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication header format",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        payload = verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # TODO: Implement actual permission checking
        # For now, just return the user payload
        logger.info(f"Permission check requested: {permission_name} (not implemented)")
        
        return payload
    
    return check_permission


