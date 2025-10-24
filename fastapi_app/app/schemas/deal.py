"""
Deal-related Pydantic schemas
"""

from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

class DealCreate(BaseModel):
    """Deal creation request model - complete schema matching frontend DefaultValues"""
    property_id: str
    lead_id: str
    deal_type: str
    buyer_id: str
    seller_id: str
    inspection_period: str
    purchase_price: str
    sale_price: str
    assignment_fee: str
    earnest_money: str
    contract_date: str
    closing_date: str
    financing_contingency: bool = False
    inspection_contingency: bool = False
    appraisal_contingency: bool = False
    title_contingency: bool = False
    notes: str = ""

class DealUpdate(BaseModel):
    """Deal update request model - all fields optional for partial updates"""
    property_id: Optional[str] = None
    lead_id: Optional[str] = None
    deal_type: Optional[str] = None
    buyer_id: Optional[str] = None
    seller_id: Optional[str] = None
    inspection_period: Optional[str] = None
    purchase_price: Optional[str] = None
    sale_price: Optional[str] = None
    assignment_fee: Optional[str] = None
    earnest_money: Optional[str] = None
    contract_date: Optional[str] = None
    closing_date: Optional[str] = None
    financing_contingency: Optional[bool] = None
    inspection_contingency: Optional[bool] = None
    appraisal_contingency: Optional[bool] = None
    title_contingency: Optional[bool] = None
    notes: Optional[str] = None

class DealResponse(BaseModel):
    """Deal response model - complete schema matching frontend DefaultValues"""
    property_id: str
    lead_id: str
    deal_type: str
    buyer_id: str
    seller_id: str
    inspection_period: str
    purchase_price: str
    sale_price: str
    assignment_fee: str
    earnest_money: str
    contract_date: str
    closing_date: str
    financing_contingency: bool
    inspection_contingency: bool
    appraisal_contingency: bool
    title_contingency: bool
    notes: str
    
    # System Fields
    id: int
    status: str
    created_at: str
    updated_at: str

class DealCreateRequest(BaseModel):
    """Deal creation request model - alias for DealCreate"""
    property_id: str
    lead_id: str
    deal_type: str
    buyer_id: str
    seller_id: str
    inspection_period: str
    purchase_price: str
    sale_price: str
    assignment_fee: str
    earnest_money: str
    contract_date: str
    closing_date: str
    financing_contingency: bool = False
    inspection_contingency: bool = False
    appraisal_contingency: bool = False
    title_contingency: bool = False
    notes: str = ""

class DealUpdateRequest(BaseModel):
    """Deal update request model - alias for DealUpdate"""
    property_id: Optional[str] = None
    lead_id: Optional[str] = None
    deal_type: Optional[str] = None
    buyer_id: Optional[str] = None
    seller_id: Optional[str] = None
    inspection_period: Optional[str] = None
    purchase_price: Optional[str] = None
    sale_price: Optional[str] = None
    assignment_fee: Optional[str] = None
    earnest_money: Optional[str] = None
    contract_date: Optional[str] = None
    closing_date: Optional[str] = None
    financing_contingency: Optional[bool] = None
    inspection_contingency: Optional[bool] = None
    appraisal_contingency: Optional[bool] = None
    title_contingency: Optional[bool] = None
    notes: Optional[str] = None

class DealBase(BaseModel):
    """Base deal schema"""
    property_id: str
    lead_id: str
    deal_type: str
    buyer_id: str
    seller_id: str
    inspection_period: str
    purchase_price: str
    sale_price: str
    assignment_fee: str
    earnest_money: str
    contract_date: str
    closing_date: str
    financing_contingency: bool
    inspection_contingency: bool
    appraisal_contingency: bool
    title_contingency: bool
    notes: str

class DealListResponse(BaseModel):
    """Deal list response schema"""
    deals: List[DealResponse]
    total: int
    page: int
    limit: int
    has_next: bool
    has_prev: bool

class DealMilestone(BaseModel):
    """Deal milestone schema"""
    id: int
    deal_id: int
    title: str
    description: str
    status: str
    due_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class DealStats(BaseModel):
    """Deal statistics schema"""
    total_deals: int
    pending_deals: int
    closed_deals: int
    total_value: Decimal
    average_deal_value: Decimal
    deals_by_type: Dict[str, int]
    deals_by_status: Dict[str, int]
    monthly_deals: List[Dict[str, Any]]