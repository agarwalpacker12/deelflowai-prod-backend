"""
Payment-related Pydantic schemas
"""

from pydantic import BaseModel, validator, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

class PaymentIntentCreate(BaseModel):
    """Payment intent creation request model"""
    amount: Decimal
    currency: str = "usd"
    payment_method_types: List[str] = ["card"]
    metadata: Optional[Dict[str, Any]] = None
    description: Optional[str] = None

class PaymentConfirm(BaseModel):
    """Payment confirmation request model"""
    payment_intent_id: str
    payment_method_id: str
    return_url: Optional[str] = None

class PaymentIntentResponse(BaseModel):
    """Payment intent response model"""
    id: str
    amount: Decimal
    currency: str
    status: str
    client_secret: str
    payment_method_types: List[str]
    metadata: Dict[str, Any]
    description: Optional[str]
    created_at: datetime

class PaymentResponse(BaseModel):
    """Payment response model"""
    id: str
    amount: Decimal
    currency: str
    status: str
    payment_method: Dict[str, Any]
    receipt_url: Optional[str] = None
    created_at: datetime

class SubscriptionResponse(BaseModel):
    """Subscription response model"""
    id: str
    status: str
    current_period_start: datetime
    current_period_end: datetime
    plan: Dict[str, Any]
    customer: Dict[str, Any]
    created_at: datetime

class PaymentListResponse(BaseModel):
    """Payment list response schema"""
    payments: List[PaymentResponse]
    total: int
    page: int
    limit: int
    has_next: bool
    has_prev: bool

class PaymentStats(BaseModel):
    """Payment statistics schema"""
    total_payments: int
    total_amount: Decimal
    successful_payments: int
    failed_payments: int
    payments_by_status: Dict[str, int]
    monthly_revenue: List[Dict[str, Any]]

class CheckoutSessionCreate(BaseModel):
    """Create Stripe checkout session request model
    
    **Minimum Required:** Only `price_id` is required. All other fields are optional.
    
    **Examples:**
    - Minimal: `{"price_id": "price_xxx"}`
    - Full: `{"price_id": "price_xxx", "success_url": "...", "cancel_url": "..."}`
    """
    price_id: str = Field(..., description="Stripe price ID for the subscription plan (REQUIRED)")
    customer_id: Optional[str] = Field(None, description="Existing Stripe customer ID (optional)")
    success_url: Optional[str] = Field(None, description="Redirect URL after successful payment (optional)")
    cancel_url: Optional[str] = Field(None, description="Redirect URL if user cancels (optional)")
    payment_gateway: str = Field("stripe", description="Payment gateway to use (default: 'stripe')")
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "description": "Minimum required (only price_id)",
                    "value": {
                        "price_id": "price_1SM4xoE0wE8Cg1knewTgPQf5"
                    }
                },
                {
                    "description": "With optional fields",
                    "value": {
                        "price_id": "price_1SM4xoE0wE8Cg1knewTgPQf5",
                        "customer_id": "cus_xxxxx",
                        "success_url": "http://localhost:3000/payment/success",
                        "cancel_url": "http://localhost:3000/payment/cancel",
                        "payment_gateway": "stripe"
                    }
                }
            ]
        }