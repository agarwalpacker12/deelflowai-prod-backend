"""
Property-related Pydantic schemas
"""

from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

class PropertyCreate(BaseModel):
    """Property creation request model - complete schema matching frontend DefaultValues"""
    # Basic Address Information
    street_address: str
    unit_apt: Optional[str] = ""
    city: str
    state: str
    zip_code: str
    county: Optional[str] = ""
    
    # Property Details
    property_type: str
    bedrooms: Optional[str] = ""
    bathrooms: Optional[str] = ""
    square_feet: Optional[str] = ""
    lot_size: Optional[str] = ""
    year_built: Optional[str] = ""
    
    # Financial Information
    purchase_price: Optional[str] = ""
    arv: Optional[str] = ""  # After Repair Value
    repair_estimate: Optional[str] = ""
    holding_costs: Optional[str] = ""
    transaction_type: Optional[str] = ""
    assignment_fee: Optional[str] = ""
    
    # Additional Information
    description: Optional[str] = ""
    seller_notes: Optional[str] = ""

class PropertyUpdate(BaseModel):
    """Property update request model - all fields optional for partial updates"""
    # Basic Address Information
    street_address: Optional[str] = None
    unit_apt: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    county: Optional[str] = None
    
    # Property Details
    property_type: Optional[str] = None
    bedrooms: Optional[str] = None
    bathrooms: Optional[str] = None
    square_feet: Optional[str] = None
    lot_size: Optional[str] = None
    year_built: Optional[str] = None
    
    # Financial Information
    purchase_price: Optional[str] = None
    arv: Optional[str] = None
    repair_estimate: Optional[str] = None
    holding_costs: Optional[str] = None
    transaction_type: Optional[str] = None
    assignment_fee: Optional[str] = None
    
    # Additional Information
    description: Optional[str] = None
    seller_notes: Optional[str] = None
    status: Optional[str] = None

class PropertyResponse(BaseModel):
    """Property response model - complete schema matching frontend DefaultValues"""
    # Basic Address Information
    street_address: str
    unit_apt: str = ""
    city: str
    state: str
    zip_code: str
    county: str = ""
    
    # Property Details
    property_type: str
    bedrooms: str = ""
    bathrooms: str = ""
    square_feet: str = ""
    lot_size: str = ""
    year_built: str = ""
    
    # Financial Information
    purchase_price: str = ""
    arv: str = ""
    repair_estimate: str = ""
    holding_costs: str = ""
    transaction_type: str = ""
    assignment_fee: str = ""
    
    # Additional Information
    description: str = ""
    seller_notes: str = ""
    
    # System Fields
    id: int
    status: str
    ai_analysis: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: str

class PropertyCreateRequest(BaseModel):
    """Property creation request model - alias for PropertyCreate"""
    # Basic Address Information
    street_address: str
    unit_apt: Optional[str] = ""
    city: str
    state: str
    zip_code: str
    county: Optional[str] = ""
    
    # Property Details
    property_type: str
    bedrooms: Optional[str] = ""
    bathrooms: Optional[str] = ""
    square_feet: Optional[str] = ""
    lot_size: Optional[str] = ""
    year_built: Optional[str] = ""
    
    # Financial Information
    purchase_price: Optional[str] = ""
    arv: Optional[str] = ""
    repair_estimate: Optional[str] = ""
    holding_costs: Optional[str] = ""
    transaction_type: Optional[str] = ""
    assignment_fee: Optional[str] = ""
    
    # Additional Information
    description: Optional[str] = ""
    seller_notes: Optional[str] = ""

class PropertyUpdateRequest(BaseModel):
    """Property update request model - alias for PropertyUpdate"""
    # Basic Address Information
    street_address: Optional[str] = None
    unit_apt: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    county: Optional[str] = None
    
    # Property Details
    property_type: Optional[str] = None
    bedrooms: Optional[str] = None
    bathrooms: Optional[str] = None
    square_feet: Optional[str] = None
    lot_size: Optional[str] = None
    year_built: Optional[str] = None
    
    # Financial Information
    purchase_price: Optional[str] = None
    arv: Optional[str] = None
    repair_estimate: Optional[str] = None
    holding_costs: Optional[str] = None
    transaction_type: Optional[str] = None
    assignment_fee: Optional[str] = None
    
    # Additional Information
    description: Optional[str] = None
    seller_notes: Optional[str] = None

class PropertyBase(BaseModel):
    """Base property schema"""
    street_address: str
    city: str
    state: str
    zip_code: str
    property_type: str
    bedrooms: Optional[str] = ""
    bathrooms: Optional[str] = ""
    square_feet: Optional[str] = ""
    lot_size: Optional[str] = ""
    year_built: Optional[str] = ""
    description: Optional[str] = ""

class PropertyListResponse(BaseModel):
    """Property list response schema"""
    properties: List[PropertyResponse]
    total: int
    page: int
    limit: int
    has_next: bool
    has_prev: bool

class PropertyAIAnalysis(BaseModel):
    """Property AI analysis schema"""
    property_id: int
    ai_confidence: float
    distress_level: float
    motivation: str
    timeline: str
    roi_percent: float
    cap_rate: float
    cash_flow: float
    market_stability_score: float
    comparables_confidence: float
    analysis_date: datetime

class PropertyStats(BaseModel):
    """Property statistics schema"""
    total_properties: int
    active_properties: int
    sold_properties: int
    average_price: Decimal
    price_range: Dict[str, Decimal]
    properties_by_type: Dict[str, int]
    top_cities: List[Dict[str, Any]]