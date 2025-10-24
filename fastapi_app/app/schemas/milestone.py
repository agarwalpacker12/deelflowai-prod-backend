"""
Deal Milestone-related Pydantic schemas
"""

from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class MilestoneCreate(BaseModel):
    """Deal milestone creation request model - complete schema matching frontend DefaultValues"""
    deal_id: str
    milestone_type: str
    title: str
    description: str
    due_date: str
    is_critical: bool = False

class MilestoneUpdate(BaseModel):
    """Deal milestone update request model - all fields optional for partial updates"""
    deal_id: Optional[str] = None
    milestone_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    is_critical: Optional[bool] = None

class MilestoneResponse(BaseModel):
    """Deal milestone response model - complete schema matching frontend DefaultValues"""
    deal_id: str
    milestone_type: str
    title: str
    description: str
    due_date: str
    is_critical: bool
    
    # System Fields
    id: int
    status: str
    created_at: str
    updated_at: str

class MilestoneCreateRequest(BaseModel):
    """Deal milestone creation request model - alias for MilestoneCreate"""
    deal_id: str
    milestone_type: str
    title: str
    description: str
    due_date: str
    is_critical: bool = False

class MilestoneUpdateRequest(BaseModel):
    """Deal milestone update request model - alias for MilestoneUpdate"""
    deal_id: Optional[str] = None
    milestone_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    is_critical: Optional[bool] = None

class MilestoneBase(BaseModel):
    """Base deal milestone schema"""
    deal_id: str
    milestone_type: str
    title: str
    description: str
    due_date: str
    is_critical: bool

class MilestoneListResponse(BaseModel):
    """Deal milestone list response schema"""
    milestones: List[MilestoneResponse]
    total: int
    page: int
    limit: int
    has_next: bool
    has_prev: bool

class MilestoneStats(BaseModel):
    """Deal milestone statistics schema"""
    total_milestones: int
    completed_milestones: int
    pending_milestones: int
    overdue_milestones: int
    critical_milestones: int
    milestones_by_type: Dict[str, int]
    completion_rate: float
