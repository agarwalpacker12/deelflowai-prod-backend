"""
Analytics-related Pydantic schemas
"""

from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

class DashboardMetrics(BaseModel):
    """Dashboard metrics schema"""
    total_revenue: Decimal
    active_users: int
    total_properties: int
    total_leads: int
    total_deals: int
    monthly_profit: Decimal
    voice_calls_count: int
    ai_conversations: int
    compliance_percentage: float
    system_health: str
    last_updated: datetime

class BusinessMetrics(BaseModel):
    """Business metrics schema"""
    revenue_growth: float
    user_growth: float
    property_growth: float
    lead_conversion_rate: float
    deal_success_rate: float
    profit_margin: float
    customer_satisfaction: float
    market_share: float

class AIAnalytics(BaseModel):
    """AI analytics schema"""
    vision_accuracy: float
    nlp_accuracy: float
    voice_success_rate: float
    blockchain_success_rate: float
    overall_ai_performance: float
    ai_usage_trends: Dict[str, Any]
    cost_per_analysis: Decimal
    roi_from_ai: float

class ActivityFeed(BaseModel):
    """Activity feed schema"""
    id: int
    user_id: int
    action_type: str
    description: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None

class ComplianceStatus(BaseModel):
    """Compliance status schema"""
    compliance_percentage: float
    audit_trail: str
    system_health: str
    last_audit: datetime
    violations: List[Dict[str, Any]] = []
    recommendations: List[str] = []

class RevenueMetrics(BaseModel):
    """Revenue metrics schema"""
    period: str
    total_revenue: Decimal
    revenue_growth: float
    revenue_by_source: Dict[str, Decimal]
    monthly_breakdown: List[Dict[str, Any]]
    projected_revenue: Decimal

class UserMetrics(BaseModel):
    """User metrics schema"""
    total_users: int
    active_users: int
    new_users: int
    user_retention: float
    users_by_role: Dict[str, int]
    user_activity: List[Dict[str, Any]]

class CampaignMetrics(BaseModel):
    """Campaign metrics schema"""
    total_campaigns: int
    active_campaigns: int
    completed_campaigns: int
    total_leads_generated: int
    conversion_rate: float
    roi_percentage: float
    cost_per_lead: Decimal
    revenue_generated: Decimal

class LeadMetrics(BaseModel):
    """Lead metrics schema"""
    total_leads: int
    new_leads: int
    qualified_leads: int
    converted_leads: int
    conversion_rate: float
    leads_by_source: Dict[str, int]
    average_lead_value: Decimal
    lead_quality_score: float

class DealMetrics(BaseModel):
    """Deal metrics schema"""
    total_deals: int
    pending_deals: int
    closed_deals: int
    total_deal_value: Decimal
    average_deal_value: Decimal
    deal_success_rate: float
    deals_by_type: Dict[str, int]
    monthly_deals: List[Dict[str, Any]]
