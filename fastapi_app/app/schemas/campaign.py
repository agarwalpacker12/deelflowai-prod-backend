"""
Campaign-related Pydantic schemas
"""

from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from decimal import Decimal

class CampaignCreate(BaseModel):
    """Campaign creation request model - complete schema matching Swagger documentation"""
    # Basic campaign information
    name: str
    campaign_type: str = "new"
    channel: List[str] = ["email"]
    budget: float
    scheduled_at: str
    subject_line: str
    email_content: str
    use_ai_personalization: bool = False
    status: str = "active"
    
    # Geographic scope (for general campaigns) - support both formats
    geographic_scope_type: str = "zip"
    geographic_scope_values: List[str] = []
    geographic_scope: Optional[Dict[str, Any]] = None  # Support object format from frontend
    
    # Basic property filters
    location: str
    property_type: str
    minimum_equity: float
    min_price: float
    max_price: float
    distress_indicators: List[str] = []
    
    # Buyer Finder - Demographic Details
    last_qualification: str = ""
    age_range: str = ""
    ethnicity: str = ""
    salary_range: str = ""
    marital_status: str = ""
    employment_status: str = ""
    home_ownership_status: str = ""
    
    # Buyer Finder - Geographic Details
    buyer_country: str = ""
    buyer_state: str = ""
    buyer_counties: str = ""
    buyer_city: str = ""
    buyer_districts: str = ""
    buyer_parish: str = ""
    
    # Seller Finder - Geographic Details
    seller_country: str = ""
    seller_state: str = ""
    seller_counties: str = ""
    seller_city: str = ""
    seller_districts: str = ""
    seller_parish: str = ""
    
    # Seller Finder - Additional Fields
    property_year_built_min: Optional[Union[int, str]] = None
    property_year_built_max: Optional[Union[int, str]] = None
    seller_keywords: str = ""

class CampaignUpdate(BaseModel):
    """Campaign update request model - all fields optional for partial updates"""
    # Basic campaign information
    name: Optional[str] = None
    campaign_type: Optional[str] = None
    channel: Optional[List[str]] = None
    budget: Optional[float] = None
    scheduled_at: Optional[str] = None
    subject_line: Optional[str] = None
    email_content: Optional[str] = None
    use_ai_personalization: Optional[bool] = None
    status: Optional[str] = None
    
    # Geographic scope (for general campaigns)
    geographic_scope_type: Optional[str] = None
    geographic_scope_values: Optional[List[str]] = None
    
    # Basic property filters
    location: Optional[str] = None
    property_type: Optional[str] = None
    minimum_equity: Optional[float] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    distress_indicators: Optional[List[str]] = None
    
    # Buyer Finder - Demographic Details
    last_qualification: Optional[str] = None
    age_range: Optional[str] = None
    ethnicity: Optional[str] = None
    salary_range: Optional[str] = None
    marital_status: Optional[str] = None
    employment_status: Optional[str] = None
    home_ownership_status: Optional[str] = None
    
    # Buyer Finder - Geographic Details
    buyer_country: Optional[str] = None
    buyer_state: Optional[str] = None
    buyer_counties: Optional[str] = None
    buyer_city: Optional[str] = None
    buyer_districts: Optional[str] = None
    buyer_parish: Optional[str] = None
    
    # Seller Finder - Geographic Details
    seller_country: Optional[str] = None
    seller_state: Optional[str] = None
    seller_counties: Optional[str] = None
    seller_city: Optional[str] = None
    seller_districts: Optional[str] = None
    seller_parish: Optional[str] = None
    
    # Seller Finder - Additional Fields
    property_year_built_min: Optional[Union[int, str]] = None
    property_year_built_max: Optional[Union[int, str]] = None
    seller_keywords: Optional[str] = None

class CampaignResponse(BaseModel):
    """Campaign response model matching Swagger documentation"""
    # Basic campaign information
    name: str
    campaign_type: str = "new"
    channel: List[str] = ["email"]  # Array in response
    budget: str  # String in response
    scheduled_at: str
    subject_line: str
    email_content: str
    use_ai_personalization: bool = False
    status: str
    id: int
    created_at: str
    updated_at: str
    
    # Geographic scope (for general campaigns)
    geographic_scope_type: str = "zip"
    geographic_scope_values: List[str] = []
    
    # Basic property filters
    location: str
    property_type: str
    minimum_equity: str  # String in response
    min_price: str  # String in response
    max_price: str  # String in response
    distress_indicators: List[str] = []
    
    # Buyer Finder - Demographic Details
    last_qualification: str = ""
    age_range: str = ""
    ethnicity: str = ""
    salary_range: str = ""
    marital_status: str = ""
    employment_status: str = ""
    home_ownership_status: str = ""
    
    # Buyer Finder - Geographic Details
    buyer_country: str = ""
    buyer_state: str = ""
    buyer_counties: str = ""
    buyer_city: str = ""
    buyer_districts: str = ""
    buyer_parish: str = ""
    
    # Seller Finder - Geographic Details
    seller_country: str = ""
    seller_state: str = ""
    seller_counties: str = ""
    seller_city: str = ""
    seller_districts: str = ""
    seller_parish: str = ""
    
    # Seller Finder - Additional Fields
    property_year_built_min: Optional[Union[int, str]] = None
    property_year_built_max: Optional[Union[int, str]] = None
    seller_keywords: str = ""

class CampaignListResponse(BaseModel):
    """Campaign list response model matching Swagger documentation"""
    campaigns: List[CampaignResponse]
    total: int
    page: int
    limit: int
    has_next: bool
    has_prev: bool

class CampaignBase(BaseModel):
    """Base campaign schema for response models"""
    name: str
    campaign_type: str
    channel: List[str]
    budget: float
    scheduled_at: str
    subject_line: str
    email_content: str
    use_ai_personalization: bool
    status: str
    geographic_scope_type: str
    geographic_scope_values: Union[str, List[str]]
    location: str
    property_type: str
    minimum_equity: float
    min_price: float
    max_price: float
    distress_indicators: List[str]
    last_qualification: str
    age_range: str
    ethnicity: str
    salary_range: str
    marital_status: str
    employment_status: str
    home_ownership_status: str
    buyer_country: str
    buyer_state: str
    buyer_counties: str
    buyer_city: str
    buyer_districts: str
    buyer_parish: str
    seller_country: str
    seller_state: str
    seller_counties: str
    seller_city: str
    seller_districts: str
    seller_parish: str
    property_year_built_min: Optional[str] = None
    property_year_built_max: Optional[str] = None
    seller_keywords: str

class CampaignResponse(CampaignBase):
    """Campaign response schema"""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CampaignPerformance(BaseModel):
    """Campaign performance metrics schema"""
    campaign_id: int
    total_sent: int
    total_delivered: int
    total_opened: int
    total_clicked: int
    total_converted: int
    open_rate: float
    click_rate: float
    conversion_rate: float
    roi_percentage: float
    cost_per_lead: Decimal
    revenue_generated: Decimal

class CampaignStats(BaseModel):
    """Campaign statistics schema"""
    total_campaigns: int
    active_campaigns: int
    completed_campaigns: int
    total_leads_generated: int
    total_revenue: Decimal
    average_roi: float
    top_performing_channels: List[Dict[str, Any]]
