"""
Organization-related Pydantic schemas
"""

from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class OrganizationBase(BaseModel):
    """Base organization schema"""
    name: str
    slug: str
    subscription_status: str = "new"

class OrganizationCreate(OrganizationBase):
    """Organization creation schema"""
    pass

class OrganizationUpdate(BaseModel):
    """Organization update schema"""
    name: Optional[str] = None
    slug: Optional[str] = None
    subscription_status: Optional[str] = None

class OrganizationResponse(OrganizationBase):
    """Organization response schema"""
    id: int
    uuid: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class OrganizationStats(BaseModel):
    """Organization statistics schema"""
    total_organizations: int
    active_subscriptions: int
    subscription_distribution: dict
    total_users: int
    total_campaigns: int
