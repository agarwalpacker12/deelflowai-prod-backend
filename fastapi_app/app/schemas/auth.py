"""
Authentication-related Pydantic schemas
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from app.schemas.user import UserResponse

class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    """Token data schema"""
    email: Optional[str] = None

class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    """Registration request schema"""
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    organization_id: Optional[int] = None
    organization: Optional[Dict[str, Any]] = None

class RegisterRequestV2(BaseModel):
    """Registration request model v2"""
    first_name: str
    last_name: str
    organization_name: str
    phone: Optional[str] = None
    email: str
    password: str

class PasswordResetRequest(BaseModel):
    """Password reset request schema"""
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema"""
    token: str
    new_password: str

class ChangePasswordRequest(BaseModel):
    """Change password request schema"""
    current_password: str
    new_password: str
