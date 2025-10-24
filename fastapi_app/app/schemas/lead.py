"""
Lead-related Pydantic schemas
"""

from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

class LeadCreate(BaseModel):
    """Lead creation request model - complete schema matching frontend DefaultValues"""
    first_name: str
    last_name: str
    email: str
    phone: str
    property_address: str
    property_city: str
    property_state: str
    property_zip: str
    property_type: str = "single_family"
    source: str = ""
    estimated_value: str = ""
    mortgage_balance: str = ""
    asking_price: str = ""
    preferred_contact_method: str = ""
    lead_type: str = ""
    status: str = "new"

class LeadUpdate(BaseModel):
    """Lead update request model - all fields optional for partial updates"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    property_address: Optional[str] = None
    property_city: Optional[str] = None
    property_state: Optional[str] = None
    property_zip: Optional[str] = None
    property_type: Optional[str] = None
    source: Optional[str] = None
    estimated_value: Optional[str] = None
    mortgage_balance: Optional[str] = None
    asking_price: Optional[str] = None
    preferred_contact_method: Optional[str] = None
    lead_type: Optional[str] = None
    status: Optional[str] = None

class LeadResponse(BaseModel):
    """Lead response model - complete schema matching frontend DefaultValues"""
    first_name: str
    last_name: str
    email: str
    phone: str
    property_address: str
    property_city: str
    property_state: str
    property_zip: str
    property_type: str
    source: str
    estimated_value: str
    mortgage_balance: str
    asking_price: str
    preferred_contact_method: str
    lead_type: str
    status: str
    
    # System Fields
    id: int
    ai_score: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: str

class LeadCreateRequest(BaseModel):
    """Lead creation request model - alias for LeadCreate"""
    first_name: str
    last_name: str
    email: str
    phone: str
    property_address: str
    property_city: str
    property_state: str
    property_zip: str
    property_type: str = "single_family"
    source: str = ""
    estimated_value: str = ""
    mortgage_balance: str = ""
    asking_price: str = ""
    preferred_contact_method: str = ""
    lead_type: str = ""
    status: str = "new"

class LeadUpdateRequest(BaseModel):
    """Lead update request model - alias for LeadUpdate"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    property_address: Optional[str] = None
    property_city: Optional[str] = None
    property_state: Optional[str] = None
    property_zip: Optional[str] = None
    property_type: Optional[str] = None
    source: Optional[str] = None
    estimated_value: Optional[str] = None
    mortgage_balance: Optional[str] = None
    asking_price: Optional[str] = None
    preferred_contact_method: Optional[str] = None
    lead_type: Optional[str] = None
    status: Optional[str] = None

class LeadBase(BaseModel):
    """Base lead schema"""
    first_name: str
    last_name: str
    email: str
    phone: str
    property_address: str
    property_city: str
    property_state: str
    property_zip: str
    property_type: str
    source: str
    estimated_value: str
    mortgage_balance: str
    asking_price: str
    preferred_contact_method: str
    lead_type: str
    status: str

class LeadListResponse(BaseModel):
    """Lead list response schema"""
    leads: List[LeadResponse]
    total: int
    page: int
    limit: int
    has_next: bool
    has_prev: bool

class LeadStats(BaseModel):
    """Lead statistics schema"""
    total_leads: int
    new_leads: int
    qualified_leads: int
    converted_leads: int
    leads_by_source: dict
    average_motivation_score: float
    top_cities: List[Dict[str, Any]]

class DiscoveredLeadResponse(BaseModel):
    """Discovered lead response model"""
    owner_name: str
    address: str
    city: str
    state: str
    zipcode: str
    source: str
    details: str
    motivation_score: int
    property_condition: str
    financial_situation: str
    timeline_urgency: str
    negotiation_style: str
    id: int
    created_at: str
    updated_at: str

class DiscoveredLeadBase(BaseModel):
    """Base discovered lead schema"""
    owner_name: Optional[str] = None
    address: str
    city: Optional[str] = None
    state: Optional[str] = None
    zipcode: Optional[str] = None
    source: str
    details: Optional[str] = None
    motivation_score: float = 0.0
    property_condition: Optional[str] = None
    financial_situation: Optional[str] = None
    timeline_urgency: Optional[str] = None
    negotiation_style: Optional[str] = None