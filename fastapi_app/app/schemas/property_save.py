"""
Property Save-related Pydantic schemas
"""

from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class PropertySaveCreate(BaseModel):
    """Property save creation request model"""
    property_id: int
    user_id: Optional[int] = None
    notes: Optional[str] = ""

class PropertySaveUpdate(BaseModel):
    """Property save update request model - all fields optional for partial updates"""
    property_id: Optional[int] = None
    user_id: Optional[int] = None
    notes: Optional[str] = None

class PropertySaveResponse(BaseModel):
    """Property save response model"""
    property_id: int
    user_id: int
    notes: str
    
    # System Fields
    id: int
    created_at: str
    updated_at: str

class PropertySaveListResponse(BaseModel):
    """Property save list response schema"""
    property_saves: List[PropertySaveResponse]
    total: int
    page: int
    limit: int
    has_next: bool
    has_prev: bool

class PropertySaveStats(BaseModel):
    """Property save statistics schema"""
    total_saves: int
    saves_by_user: Dict[str, int]
    most_saved_properties: List[Dict[str, Any]]
    recent_saves: List[PropertySaveResponse]
