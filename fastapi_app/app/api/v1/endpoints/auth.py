"""
Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, create_refresh_token, verify_password, get_password_hash
from app.core.exceptions import AuthenticationError, ValidationError
from app.schemas.auth import Token, LoginRequest, RegisterRequest, UserResponse
from app.services.user_service import UserService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """User login endpoint"""
    try:
        user_service = UserService()
        user = await user_service.authenticate_user(login_data.email, login_data.password)
        
        if not user:
            raise AuthenticationError("Invalid email or password")
        
        if not user.is_active:
            raise AuthenticationError("Account is deactivated")
        
        # Create tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.from_orm(user)
        )
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

@router.post("/register", response_model=UserResponse)
async def register(register_data: RegisterRequest):
    """User registration endpoint"""
    try:
        user_service = UserService()
        
        # Check if user already exists
        existing_user = await user_service.get_user_by_email(register_data.email)
        if existing_user:
            raise ValidationError("User with this email already exists")
        
        # Create user
        user = await user_service.create_user(register_data)
        
        return UserResponse.from_orm(user)
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    """Refresh access token"""
    try:
        from app.core.security import verify_token
        
        payload = verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise AuthenticationError("Invalid refresh token")
        
        user_id = payload.get("sub")
        user_service = UserService()
        user = await user_service.get_user_by_id(int(user_id))
        
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")
        
        # Create new access token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.from_orm(user)
        )
        
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.post("/logout")
async def logout():
    """User logout endpoint"""
    return {"message": "Successfully logged out"}
