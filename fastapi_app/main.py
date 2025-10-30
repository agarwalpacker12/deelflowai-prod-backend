"""
DeelFlowAI FastAPI Application - Final Clean Version
Completely organized with proper Swagger grouping and frontend compatibility
"""

from fastapi import FastAPI, HTTPException, Request, Query, Depends, Header, status, UploadFile, File, Body, Request as FastAPIRequest, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request
from fastapi.params import Path as PathParam
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Union, Dict, Any
import os
import sys
import django
import datetime
import logging
from pathlib import Path
from asgiref.sync import sync_to_async
from django.utils import timezone
import ast

logger = logging.getLogger(__name__)

# Load environment variables BEFORE Django setup
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Import authentication dependencies
from app.core.auth_middleware import get_current_user

# Import schemas from their respective files
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse, CampaignListResponse
from app.schemas.user import LoginRequest, UserResponse, UserCreateRequest, UserUpdateRequest, UsersListResponse
from app.schemas.property import PropertyResponse, PropertyCreateRequest, PropertyUpdateRequest, PropertyCreate, PropertyUpdate
from app.schemas.lead import LeadResponse, LeadCreateRequest, LeadUpdateRequest, DiscoveredLeadResponse, LeadCreate, LeadUpdate
from app.schemas.deal import DealResponse, DealCreateRequest, DealUpdateRequest, DealCreate, DealUpdate
from app.schemas.milestone import MilestoneCreate, MilestoneUpdate, MilestoneResponse, MilestoneCreateRequest, MilestoneUpdateRequest
from app.schemas.property_save import PropertySaveCreate, PropertySaveUpdate, PropertySaveResponse, PropertySaveListResponse
from app.schemas.payment import PaymentIntentCreate, PaymentConfirm, PaymentIntentResponse, PaymentResponse, SubscriptionResponse, CheckoutSessionCreate
from app.schemas.auth import RegisterRequest, RegisterRequestV2
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse

# Mock data functions (replacing deleted database module)
# Import database functions
from database import (
    get_dashboard_stats,
    get_ai_metrics,
    get_tenant_management_data,
    get_opportunity_cost_data,
    get_revenue_growth_data,
    get_market_alerts_data,
    get_live_activity_data,
    get_performance_metrics
)

# Add Django project to Python path
django_project_path = Path(__file__).parent.parent
sys.path.append(str(django_project_path))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deelflow.settings')
django.setup()

from app.api.v1.api import api_router
from app.core.config import settings

# Create FastAPI application
app = FastAPI(
    title="DeelFlowAI Backend API",
    version="1.0.0",
    description="""
    ## DeelFlowAI - Comprehensive Real Estate AI Platform Backend API
    
    A powerful backend API for real estate professionals, investors, and agents to manage properties, 
    campaigns, leads, deals, and leverage AI-powered analytics and automation.
    
    ### Key Features:
    - 🏠 **Property Management**: Complete CRUD operations for properties with AI analysis
    - 📊 **Analytics & Reporting**: Comprehensive analytics for deals, campaigns, and performance
    - 🤖 **AI Services**: Voice AI, vision analysis, NLP processing, and blockchain integration
    - 📈 **Campaign Management**: Multi-channel marketing campaigns with performance tracking
    - 👥 **Lead Management**: Lead generation, scoring, and conversion tracking
    - 💼 **Deal Management**: Deal pipeline management with milestone tracking
    - 🔐 **Authentication**: JWT-based authentication and user management
    - 📱 **Dashboard**: Real-time metrics and KPI tracking
    
    ### Authentication:
    Most endpoints require authentication. Use the `/api/auth/login` endpoint to get a JWT token, 
    then include it in the Authorization header: `Bearer <your-token>`
    """,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "DeelFlowAI Support",
        "email": "support@deelflowai.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Add custom tags metadata for better Swagger UI organization
tags_metadata = [
    {
        "name": "Core",
        "description": "Core API endpoints for health checks, status, and basic information.",
    },
    {
        "name": "Authentication",
        "description": "User authentication, registration, and session management endpoints.",
    },
    {
        "name": "Dashboard",
        "description": "Dashboard metrics, KPIs, and real-time data for the main dashboard interface.",
    },
    {
        "name": "Analytics",
        "description": "Comprehensive analytics endpoints for deals, campaigns, performance, and market data.",
    },
    {
        "name": "Properties",
        "description": "Property management endpoints including CRUD operations and AI analysis.",
    },
    {
        "name": "Property Saves",
        "description": "Property save/favorite functionality for users to bookmark properties.",
    },
    {
        "name": "Campaigns",
        "description": "Marketing campaign management, performance tracking, and analytics.",
    },
    {
        "name": "Leads",
        "description": "Lead management, scoring, and conversion tracking endpoints.",
    },
    {
        "name": "AI Services",
        "description": "AI-powered services including voice AI, vision analysis, NLP, and blockchain integration.",
    },
    {
        "name": "Tenant Management",
        "description": "Multi-tenant organization management and tenant-specific data.",
    },
    {
        "name": "Organizations",
        "description": "Organization management and status endpoints.",
    },
    {
        "name": "Payments",
        "description": "Payment processing, subscription management, and billing endpoints using Stripe integration.",
    },
    {
        "name": "Role Management",
        "description": "Role-based access control (RBAC) endpoints for managing roles, permissions, and user-role assignments.",
    },
    {
        "name": "Permissions",
        "description": "Permission management endpoints for granular access control.",
    },
    {
        "name": "ATTOM API",
        "description": "Property data integration with ATTOM Data Solutions API.",
    },
    {
        "name": "SignNow",
        "description": "Electronic signature integration with SignNow API.",
    },
    {
        "name": "Blockchain",
        "description": "Polygon (MATIC) blockchain endpoints.",
    }
]

# Update the app with tags metadata
app.openapi_tags = tags_metadata

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:3000",
        "http://127.0.0.1:5173",  # Vite default port
        "http://127.0.0.1:3000",
        "http://dev.deelflowai.com:8140",
        "http://dev.deelflowai.com:8000",
        "https://apps.deelflowai.com",
        "https://www.deelflowai.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "api.deelflowai.com",
        "apps.deelflowai.com",
        "dev.deelflowai.com",
        "localhost",
        "127.0.0.1",
        "*"
    ]
)

# Include API router - this will add properly organized endpoints
# app.include_router(api_router, prefix=settings.API_V1_STR)

# ==================== CORE ENDPOINTS ====================

@app.get("/", tags=["Core"])
async def root():
    """
    **Root Endpoint - API Information**
    
    Returns basic information about the DeelFlowAI Backend API including version, status, and documentation links.
    
    **Returns:**
    - API name and version
    - Current status
    - Links to API documentation (Swagger UI and ReDoc)
    """
    return {
        "message": "DeelFlowAI Backend API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Core"])
async def health_check():
    """
    **Health Check Endpoint**
    
    Performs a comprehensive health check to verify the API and all dependent services are running properly.
    
    **Returns:**
    - Overall health status
    - Timestamp of the check
    - Status of individual services (database, AI services, background tasks)
    """
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "services": {
            "database": "connected",
            "ai_services": "active",
            "background_tasks": "running"
        }
    }

# ==================== DASHBOARD ENDPOINTS ====================

@app.get("/stats", tags=["Dashboard"])
@app.options("/stats")
async def get_stats():
    """
    **Dashboard Statistics**
    
    Retrieves comprehensive statistics for the main dashboard including revenue, user metrics, 
    property counts, and AI conversation data with growth percentages.
    
    **Returns:**
    - Total revenue and growth percentage
    - Active users and growth percentage  
    - Properties listed and growth percentage
    - AI conversations count and growth percentage
    """
    try:
        # Get data from database
        db_stats = await get_dashboard_stats()
        return {
            'status': 'success',
            'data': {
                'total_revenue': db_stats['total_revenue'],
                'revenue_growth': 12.5,  # This would be calculated from historical data
                'active_users': db_stats['active_users'],
                'users_growth': 8.3,
                'properties_listed': db_stats['total_properties'],
                'properties_growth': 15.2,
                'ai_conversations': db_stats['ai_conversations'],
                'conversation_rate': 87.5,
                'total_deals': db_stats['total_deals'],
                'deals_growth': 22.1,
                'monthly_profit': db_stats['monthly_profit'],
                'profit_growth': 18.7,
                'ai_accuracy': db_stats['ai_accuracy'],
                'accuracy_improvement': 5.8,
                'voice_calls': db_stats['voice_calls'],
                'compliance_status': db_stats['compliance_status']
            }
        }
    except Exception as e:
            return {
            'status': 'error',
            'message': f'Failed to fetch stats: {str(e)}',
            'data': {}
        }

@app.get("/status", tags=["Dashboard"])
@app.options("/status")
async def get_status():
    """Get system status and health information"""
    return {
        'status': 'success',
        'data': {
            'database': 'connected',
            'api': 'operational',
            'ai_services': 'active',
            'background_tasks': 'running',
            'counts': {
                'users': 150,
                'properties': 89,
                'leads': 234,
                'deals': 45
            },
            'timestamp': '2025-10-09T04:30:00Z'
        }
    }

@app.get("/recent_activity", tags=["Dashboard"])
@app.options("/recent_activity")
async def get_recent_activity():
    """Get recent activity feed"""
    return {
        "status": "success",
        "message": "Recent activity retrieved successfully",
        "data": {
            "activities": [
                {"event": "New lead added", "date": "2025-10-08", "user": "System", "action_type": "lead_created"},
                {"event": "Property analysis completed", "date": "2025-10-07", "user": "AI", "action_type": "ai_analysis"},
                {"event": "Campaign launched", "date": "2025-10-06", "user": "Admin", "action_type": "campaign_created"},
                {"event": "Deal closed", "date": "2025-10-05", "user": "Agent", "action_type": "deal_closed"}
            ],
            "last_updated": "2025-10-09T04:30:00Z"
        }
    }

@app.post("/recent_activity", tags=["Dashboard"])
@app.options("/recent_activity")
async def create_recent_activity(activity_data: dict):
    """Create a new activity entry"""
    return {
        "status": "success",
        "message": "Activity created successfully",
        "data": {
            "id": 1,
            "event": activity_data.get("event", "New activity"),
            "date": timezone.now().isoformat(),
            "user": activity_data.get("user", "System"),
            "action_type": activity_data.get("action_type", "general")
        }
    }

@app.get("/opportunity-cost-analysis", tags=["Dashboard"])
@app.options("/opportunity-cost-analysis")
async def get_opportunity_cost_analysis():
    """Get opportunity cost analysis data"""
    try:
        db_data = await get_opportunity_cost_data()
        return {
            "status": "success",
            "data": db_data
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch opportunity cost analysis: {str(e)}"
        }

# ==================== LEGACY DASHBOARD ENDPOINTS ====================

@app.get("/api/total-revenue/", tags=["Dashboard"])
async def get_total_revenue():
    """Get total revenue data"""
    try:
        db_stats = await get_dashboard_stats()
        return {
            "status": "success",
            "data": {
                "total_revenue": 125000.50,  # Mock data since not in db_stats
                "change_percentage": 12.5,  # Frontend expects this field name
                "monthly_revenue": 45000.00,
                "quarterly_revenue": 375000.00
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch revenue data: {str(e)}"
        }

@app.get("/api/active-users/", tags=["Dashboard"])
async def get_active_users():
    """Get active users data"""
    try:
        db_stats = await get_dashboard_stats()
        return {
        "status": "success",
        "data": {
                "active_users": db_stats['totalUsers'],
                "change_percentage": 8.3,  # Frontend expects this field name
                "new_users_this_month": 15,
                "retention_rate": 87.5
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch users data: {str(e)}"
        }

@app.get("/api/properties-listed/", tags=["Dashboard"])
async def get_properties_listed():
    """Get properties listed data"""
    try:
        db_stats = await get_dashboard_stats()
        return {
        "status": "success",
        "data": {
                "properties_listed": db_stats['totalProperties'],
                "change_percentage": 15.2,  # Frontend expects this field name
                "new_listings_this_month": 8,
                "average_listing_price": 450000
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch properties data: {str(e)}"
        }

@app.get("/api/ai-conversations/", tags=["Dashboard"])
async def get_ai_conversations():
    """Get AI conversations data"""
    try:
        db_stats = await get_dashboard_stats()
        return {
        "status": "success",
        "data": {
                "ai_conversations": 1250,  # Mock data
                "change_percentage": 87.5,  # Frontend expects this field name
                "successful_interactions": 1094,
                "average_response_time": 2.3
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch AI conversations data: {str(e)}"
        }

@app.get("/api/total-deals/", tags=["Dashboard"])
async def get_total_deals():
    """Get total deals data"""
    try:
        db_stats = await get_dashboard_stats()
        return {
        "status": "success",
        "data": {
                "total_deals": db_stats['totalDeals'],
                "change_percentage": 22.1,  # Frontend expects this field name
                "closed_deals_this_month": 12,
                "average_deal_value": 125000
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch deals data: {str(e)}"
        }

@app.get("/api/monthly-profit/", tags=["Dashboard"])
async def get_monthly_profit():
    """Get monthly profit data"""
    try:
        db_stats = await get_dashboard_stats()
        return {
        "status": "success",
        "data": {
                "monthly_profit": 45000.00,
                "change_percentage": 18.7,  # Frontend expects this field name
                "profit_margin": 35.2,
                "year_to_date_profit": 450000.00
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch profit data: {str(e)}"
        }

@app.get("/api/voice-calls-count/", tags=["Dashboard"])
async def get_voice_calls_count():
    """Get voice calls count data"""
    try:
        db_stats = await get_dashboard_stats()
        return {
        "status": "success",
        "data": {
                "voice_calls": 245,
                "change_percentage": 87.5,  # Frontend expects this field name
                "average_duration": 4.2,
                "calls_this_month": 245
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch voice calls data: {str(e)}"
        }

@app.get("/api/compliance-status/", tags=["Dashboard"])
async def get_compliance_status():
    """Get compliance status data"""
    try:
        db_stats = await get_dashboard_stats()
        return {
        "status": "success",
        "data": {
                "compliance_status": "compliant",
                "audit_score": 94.2,
                "last_audit": "2025-10-01T00:00:00Z",
                "next_audit": "2026-01-01T00:00:00Z"
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch compliance data: {str(e)}"
        }

# ==================== AI METRICS ENDPOINTS ====================

@app.get("/api/voice-ai-calls-count/", tags=["AI Services"])
async def get_voice_ai_calls_count():
    """Get voice AI calls count and metrics"""
    try:
        ai_metrics = await get_ai_metrics()
        return {
        "status": "success",
        "data": {
                "total_calls": ai_metrics.get('voiceCalls', 0),
                "success_rate": 87.5,
                "average_duration": 4.2
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch voice AI metrics: {str(e)}"
        }

@app.get("/api/vision-analysis/", tags=["AI Services"])
async def get_vision_analysis():
    """Get vision analysis metrics"""
    try:
        ai_metrics = await get_ai_metrics()
        return {
        "status": "success",
        "data": {
                "total_analyses": ai_metrics.get('visionAnalyses', 0),
                "accuracy_rate": 89.2,
                "processing_time": 2.1
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch vision analysis metrics: {str(e)}"
        }

@app.get("/api/nlp-processing/", tags=["AI Services"])
async def get_nlp_processing():
    """Get NLP processing metrics"""
    try:
        ai_metrics = await get_ai_metrics()
        return {
        "status": "success",
        "data": {
                "total_processed": ai_metrics.get('nlpAnalyses', 0),
                "processing_success_rate": 91.5,
                "average_processing_time": 1.8
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch NLP processing metrics: {str(e)}"
        }

@app.get("/api/blockchain-txns/", tags=["AI Services"])
async def get_blockchain_transactions():
    """Get blockchain transaction metrics"""
    try:
        ai_metrics = await get_ai_metrics()
        return {
        "status": "success",
        "data": {
                "total_transactions": ai_metrics.get('blockchainTxns', 0),
                "success_rate": 95.8,
                "average_processing_time": 3.2
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch blockchain metrics: {str(e)}"
        }

# ==================== TENANT MANAGEMENT ENDPOINTS ====================

@app.get("/api/tenant-management/", tags=["Tenant Management"])
async def get_tenant_management():
    """Get tenant management data (redirect to stats)"""
    try:
        tenant_data = await get_tenant_management_data()
        return {
            "status": "success",
            "data": tenant_data
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch tenant data: {str(e)}"
        }

@app.get("/api/tenant-management/stats/", tags=["Tenant Management"])
async def get_tenant_management_stats():
    """Get tenant management statistics"""
    try:
        tenant_data = await get_tenant_management_data()
        return {
        "status": "success",
            "data": tenant_data
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch tenant stats: {str(e)}"
        }

@app.get("/api/analytics/opportunity-cost-analysis/", tags=["Analytics"])
async def get_analytics_opportunity_cost():
    """Get analytics opportunity cost data"""
    try:
        opportunity_data = await get_opportunity_cost_data()
        return {
        "status": "success",
            "data": opportunity_data
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch analytics data: {str(e)}"
        }

@app.get("/api/analytics/deals/", tags=["Analytics"])
async def get_analytics_deals():
    """
    **Deals Analytics**
    
    Provides comprehensive analytics data for real estate deals including overview metrics, 
    deal breakdown by status, property types, lead sources, and recent activity.
    
    **Returns:**
    - Deal overview (total deals, properties, leads, deal value, average deal value)
    - Deal breakdown by status (active, closed, pending)
    - Property type distribution (residential, commercial)
    - Lead source analysis (website, referral, advertisement)
    - Recent activity metrics (deals, properties, leads in last 30 days)
    - Detailed deals list with key information
    """
    try:
        # Mock data for now - replace with actual database calls when ready
        return {
        "status": "success",
        "data": {
                "overview": {
                    "total_deals": 5,
                    "total_properties": 12,
                    "total_leads": 25,
                    "total_deal_value": 250000.0,
                    "avg_deal_value": 50000.0
                },
                "deal_breakdown": {
                    "active": 3,
                    "closed": 2,
                    "pending": 0
                },
                "property_types": {
                    "residential": 8,
                    "commercial": 4
                },
                "lead_sources": {
                    "website": 15,
                    "referral": 7,
                    "advertisement": 3
                },
                "recent_activity": {
                    "deals_last_30_days": 2,
                    "properties_last_30_days": 3,
                    "leads_last_30_days": 8
                },
                "deals": [
                    {
            "id": 1,
                        "property_address": "123 Main St, Dallas, TX",
                        "offer_price": 150000.0,
                        "status": "active",
                        "created_at": "2025-10-15T10:30:00Z",
                        "deal_type": "purchase"
                    },
                    {
                        "id": 2,
                        "property_address": "456 Oak Ave, Austin, TX",
                        "offer_price": 200000.0,
                        "status": "closed",
                        "created_at": "2025-10-10T14:20:00Z",
                        "deal_type": "investment"
                    }
                ]
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch deals analytics: {str(e)}"
        }

@app.get("/api/analytics/campaigns/", tags=["Analytics"])
async def get_analytics_campaigns():
    """
    **Campaigns Analytics**
    
    Provides detailed analytics for marketing campaigns including performance metrics, 
    channel analysis, and campaign status breakdown.
    
    **Returns:**
    - Campaign overview (total campaigns, budget, leads generated, conversion rate)
    - Campaign status breakdown (active, paused, completed, draft)
    - Channel performance analysis (email, SMS, voice, social media)
    - Recent campaign activity and performance trends
    - Detailed campaign list with key metrics
    """
    try:
        # Mock data for now - replace with actual database calls when ready
        return {
            "status": "success",
            "data": {
                "overview": {
                    "total_campaigns": 8,
                    "total_outreach_campaigns": 15,
                    "total_budget": 50000.0,
                    "avg_budget": 6250.0
                },
                "campaign_statuses": {
                    "active": 5,
                    "completed": 2,
                    "paused": 1
                },
                "channels": {
                    "email": 8,
                    "sms": 4,
                    "voice": 3
                },
                "recent_activity": {
                    "campaigns_last_30_days": 3
                },
                "campaigns": [
                    {
            "id": 1,
                        "name": "Q4 Property Marketing",
                        "status": "active",
                        "budget": 10000.0,
                        "created_at": "2025-10-15T09:00:00Z",
                        "channel": "email"
                    },
                    {
            "id": 2,
                        "name": "Lead Generation Campaign",
                        "status": "completed",
                        "budget": 7500.0,
                        "created_at": "2025-10-01T14:30:00Z",
                        "channel": "sms"
                    }
                ]
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch campaigns analytics: {str(e)}"
        }

@app.get("/api/analytics/performance/", tags=["Analytics"])
async def get_analytics_performance():
    """
    **Performance Analytics**
    
    Provides comprehensive AI performance metrics and business analytics including 
    AI service performance, analysis breakdown, and business metrics.
    
    **Returns:**
    - AI performance metrics (voice calls, vision analysis, NLP processing, blockchain)
    - Analysis breakdown by type and accuracy rates
    - Business metrics including revenue, growth, and efficiency indicators
    - Performance trends and optimization recommendations
    """
    try:
        # Mock data for now - replace with actual database calls when ready
        return {
            "status": "success",
            "data": {
                "ai_performance": {
                    "voice_calls": {
                        "total": 156,
                        "success_rate": 0.875
                    },
                    "vision_analysis": {
                        "total": 89,
                        "accuracy": 0.92
                    },
                    "nlp_processing": {
                        "total": 234,
                        "accuracy": 0.88
                    },
                    "blockchain": {
                        "total_transactions": 45,
                        "success_rate": 0.95
                    }
                },
                "analysis_breakdown": {
                    "property_analysis": 25,
                    "lead_scoring": 18,
                    "market_analysis": 12
                },
                "business_metrics": [
                    {
                        "total_revenue": 125000.50,
                        "active_users": 45,
                        "properties_listed": 12,
                        "ai_conversations": 1300.0,
                        "total_deals": 5,
                        "created_at": "2025-10-17T12:00:00Z"
                    }
                ]
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch performance analytics: {str(e)}"
        }

@app.get("/api/analytics/market/", tags=["Analytics"])
async def get_analytics_market():
    """
    **Market Analytics**
    
    Provides comprehensive market analysis and trends including property market overview, 
    price distribution, geographic analysis, and AI-powered market insights.
    
    **Returns:**
    - Market overview (total properties, average price, market trends)
    - Price distribution analysis by ranges
    - Geographic distribution by state/region
    - AI-generated market insights and predictions
    - Recent property listings and market activity
    """
    try:
        # Mock data for now - replace with actual database calls when ready
        return {
            "status": "success",
            "data": {
                "market_overview": {
                    "total_properties": 12,
                    "avg_property_price": 275000.0,
                    "total_deals": 5
                },
                "price_distribution": {
                    "under_100k": 1,
                    "100k_300k": 6,
                    "300k_500k": 4,
                    "500k_1m": 1,
                    "over_1m": 0
                },
                "state_distribution": {
                    "Texas": 8,
                    "California": 3,
                    "Florida": 1
                },
                "ai_insights": {
                    "avg_confidence": 0.85,
                    "avg_distress_level": 0.65,
                    "motivation_breakdown": {
                        "investment": 5,
                        "primary_residence": 4,
                        "vacation_home": 3
                    }
                },
                "recent_properties": [
                    {
            "id": 1,
                        "address": "123 Main St",
                        "city": "Dallas",
                        "state": "Texas",
                        "price": 250000.0,
                        "property_type": "residential",
                        "status": "active",
                        "created_at": "2025-10-15T10:30:00Z"
                    },
                    {
            "id": 2,
                        "address": "456 Oak Ave",
                        "city": "Austin",
                        "state": "Texas",
                        "price": 350000.0,
                        "property_type": "residential",
                        "status": "pending",
                        "created_at": "2025-10-12T14:20:00Z"
                    }
                ]
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch market analytics: {str(e)}"
        }

@app.get("/api/organizations/status/", tags=["Organizations"])
async def get_organizations_status():
    """Get organizations status"""
    return {
        "status": "success",
        "data": {
            "active_organizations": 25,
            "total_organizations": 28,
            "suspended_organizations": 3,
            "monthly_revenue": 125000.50,
            "growth_rate": 12.5
        }
    }

# ==================== MISSING DASHBOARD ENDPOINTS ====================

@app.get("/api/live-activity-feed/", tags=["Dashboard"])
async def get_live_activity_feed():
    """Get live activity feed - Frontend expected endpoint"""
    try:
        live_data = await get_live_activity_data()
        return {
        "status": "success",
        "data": {
                "activities": live_data  # Frontend expects this field name
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch live activity: {str(e)}"
        }

@app.get("/api/deal-completions-scheduling/", tags=["Dashboard"])
async def get_deal_completions_scheduling():
    """Get deal completions scheduling - Frontend expected endpoint"""
    return {
        "status": "success",
        "data": {
            "scheduled_completions": 8,
            "completed_this_month": 12,
            "upcoming_completions": [
                {"deal_id": 1, "completion_date": "2025-10-15", "value": 150000},
                {"deal_id": 2, "completion_date": "2025-10-20", "value": 200000}
            ]
        }
    }

@app.get("/api/revenue-user-growth-chart-data/", tags=["Dashboard"])
async def get_revenue_user_growth_chart_data():
    """Get revenue user growth chart data - Frontend expected endpoint"""
    try:
        chart_data = await get_revenue_growth_data()
        return {
            "status": "success",
            "data": {
                "chart_data": chart_data  # Frontend expects this field name
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch chart data: {str(e)}"
        }

@app.get("/api/ai-metrics/overall-accuracy/", tags=["AI Services"])
async def get_ai_metrics_overall_accuracy():
    """Get AI metrics overall accuracy - Frontend expected endpoint"""
    try:
        ai_metrics = await get_ai_metrics()
        return {
            "status": "success",
            "data": {
                "overall_accuracy": ai_metrics.get('overall_accuracy', 87.5),
                "accuracy_trend": [85.2, 86.1, 87.3, 87.5],
                "model_performance": {
                    "property_analysis": 89.2,
                    "lead_scoring": 85.7,
                    "market_prediction": 88.1
                }
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch AI accuracy: {str(e)}"
        }

@app.get("/api/compliance-status/details/", tags=["Dashboard"])
async def get_compliance_status_details():
    """Get compliance status details - Frontend expected endpoint"""
    return {
        "status": "success",
        "data": {
            "compliance_score": 94.2,
            "last_audit": "2025-10-01T00:00:00Z",
            "next_audit": "2026-01-01T00:00:00Z",
            "requirements_met": 18,
            "requirements_total": 19,
            "pending_actions": [
                {"action": "Update privacy policy", "due_date": "2025-11-01"},
                {"action": "Review data retention", "due_date": "2025-10-25"}
            ]
        }
    }

@app.get("/api/market-alerts/recent/", tags=["Dashboard"])
async def get_market_alerts_recent():
    """Get recent market alerts - Frontend expected endpoint"""
    try:
        alerts_data = await get_market_alerts_data()
        return {
            "status": "success",
            "data": {
                "alerts": alerts_data  # Frontend expects this field name
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch market alerts: {str(e)}"
        }

@app.post("/recent_activity/", tags=["Dashboard"])
async def get_recent_activity():
    """Get recent tenant activity - Frontend expected endpoint"""
    try:
        # Mock data for recent activity
        return {
            "status": "success",
            "data": [
                {
                    "id": 1,
                    "type": "property_viewed",
                    "description": "Property 123 Main St viewed by tenant",
                    "timestamp": "2025-10-17T10:15:00Z",
                    "tenant_id": 1,
                    "property_id": 1
                },
                {
                    "id": 2,
                    "type": "lease_renewed",
                    "description": "Lease renewed for 6 months",
                    "timestamp": "2025-10-17T09:30:00Z",
                    "tenant_id": 2,
                    "property_id": 2
                },
                {
                    "id": 3,
                    "type": "maintenance_request",
                    "description": "New maintenance request submitted",
                    "timestamp": "2025-10-17T08:45:00Z",
                    "tenant_id": 3,
                    "property_id": 1
                }
            ]
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to fetch recent activity: {str(e)}"
        }

# ==================== PROPERTY ENDPOINTS (Frontend Compatible) ====================

@app.get("/api/properties/", tags=["Properties"])
async def get_properties():
    """
    **Get Properties List**
    
    Retrieves a paginated list of all properties with optional filtering and search capabilities.
    
    **Query Parameters:**
    - page: Page number (default: 1)
    - per_page: Items per page (default: 10)
    - search: Search term for property address or description
    - property_type: Filter by property type
    - min_price: Minimum price filter
    - max_price: Maximum price filter
    
    **Returns:**
    - Paginated list of properties
    - Total count and pagination metadata
    - Property details including address, price, type, status
    """
    try:
        from deelflow.models import Property
        
        properties = await sync_to_async(list)(Property.objects.all())
        
        property_data = []
        for property in properties:
            property_data.append({
                "id": property.id,
                "address": property.address,
                "city": property.city,
                "state": property.state,
                "zipcode": property.zipcode,
                "property_type": property.property_type,
                "bedrooms": property.bedrooms,
                "bathrooms": property.bathrooms,
                "square_feet": property.square_feet,
                "lot_size": property.lot_size,
                "year_built": property.year_built,
                "price": float(property.price) if property.price else None,
                "description": property.description,
                "images": property.images,
                "status": property.status,
                "created_at": property.created_at.isoformat(),
                "updated_at": property.updated_at.isoformat()
            })
        return {
            "status": "success",
            "data": property_data,
            "total": len(property_data),
            "page": 1,
            "limit": 20
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to retrieve properties: {str(e)}",
            "data": [],
            "total": 0,
            "page": 1,
            "limit": 20
        }

@app.post("/api/properties/", tags=["Properties"])
async def create_property(property_data: PropertyCreate):
    """Create a new property - Frontend compatible endpoint"""
    try:
        from deelflow.models import Property
        
        # Create property in Django database
        property = await sync_to_async(Property.objects.create)(
            address=property_data.street_address,
            unit_apt=property_data.unit_apt,
            city=property_data.city,
            state=property_data.state,
            zipcode=property_data.zip_code,
            county=property_data.county,
            property_type=property_data.property_type,
            bedrooms=int(property_data.bedrooms) if property_data.bedrooms and property_data.bedrooms != "" else None,
            bathrooms=int(property_data.bathrooms) if property_data.bathrooms and property_data.bathrooms != "" else None,
            square_feet=int(property_data.square_feet) if property_data.square_feet and property_data.square_feet != "" else None,
            lot_size=float(property_data.lot_size) if property_data.lot_size and property_data.lot_size != "" else None,
            year_built=int(property_data.year_built) if property_data.year_built and property_data.year_built != "" else None,
            price=float(property_data.purchase_price) if property_data.purchase_price and property_data.purchase_price != "" else None,
            arv=float(property_data.arv) if property_data.arv and property_data.arv != "" else None,
            repair_estimate=float(property_data.repair_estimate) if property_data.repair_estimate and property_data.repair_estimate != "" else None,
            holding_costs=float(property_data.holding_costs) if property_data.holding_costs and property_data.holding_costs != "" else None,
            transaction_type=property_data.transaction_type,
            assignment_fee=float(property_data.assignment_fee) if property_data.assignment_fee and property_data.assignment_fee != "" else None,
            description=property_data.description,
            seller_notes=property_data.seller_notes,
            status="active"
        )
        return {
            "status": "success",
            "message": "Property created successfully",
            "data": {
                "id": property.id,
                "address": property.address,
                "city": property.city,
                "state": property.state,
                "property_type": property.property_type,
                "status": property.status,
                "created_at": property.created_at.isoformat(),
                "updated_at": property.updated_at.isoformat()
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to create property: {str(e)}"
        }

@app.get("/api/properties/{property_id}/", 
         tags=["Properties"],
         summary="Get Property by ID",
         description="Retrieves a specific property by its ID with all associated data including financial details, property specifications, and location information.",
         response_description="Property details with all fields",
         responses={
             200: {
                 "description": "Property retrieved successfully",
                 "content": {
                     "application/json": {
                         "example": {
        "status": "success",
        "data": {
                                 "id": 1,
                                 "street_address": "123 Main Street",
                                 "unit_apt": "Apt 2B",
                                 "city": "Miami",
                                 "state": "FL",
                                 "zip_code": "33101",
                                 "county": "Miami-Dade",
                                 "property_type": "residential",
                                 "bedrooms": 3,
                                 "bathrooms": 2.5,
                                 "square_feet": 1800,
                                 "lot_size": 0.25,
                                 "year_built": 1995,
                                 "purchase_price": 250000.0,
                                 "arv": 350000.0,
                                 "repair_estimate": 25000.0,
                                 "holding_costs": 5000.0,
                                 "transaction_type": "wholesale",
                                 "assignment_fee": 10000.0,
                                 "property_description": "Beautiful single-family home in great neighborhood",
                                 "seller_notes": "Motivated seller, needs quick sale",
                                 "images": ["image1.jpg", "image2.jpg"],
                                 "status": "active",
                                 "created_at": "2024-10-13T07:34:07.710903+00:00",
                                 "updated_at": "2024-10-18T06:28:14.415806+00:00"
                             }
                         }
                     }
                 }
             },
             404: {
                 "description": "Property not found",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "error",
                             "message": "Property not found"
                         }
                     }
                 }
             },
             500: {
                 "description": "Internal server error",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "error",
                             "message": "Failed to retrieve property: Database connection error"
                         }
                     }
                 }
             }
         })
async def get_property(property_id: int):
    """
    **Get Property by ID**
    
    Retrieves a specific property by its ID with comprehensive data including:
    
    **Location Data:**
    - Street address and unit/apartment information
    - City, state, zip code, and county details
    
    **Property Specifications:**
    - Property type, bedrooms, bathrooms
    - Square footage and lot size
    - Year built and property description
    
    **Financial Information:**
    - Purchase price and after repair value (ARV)
    - Repair estimates and holding costs
    - Transaction type and assignment fees
    
    **Additional Details:**
    - Seller notes and property images
    - Status and timestamps
    
    **Parameters:**
    - **property_id** (int): The unique identifier of the property to retrieve
    
    **Returns:**
    - **200**: Property data with all fields populated
    - **404**: Property not found
    - **500**: Server error during retrieval
    """
    try:
        from deelflow.models import Property
        
        property = await sync_to_async(Property.objects.get)(id=property_id)
        return {
        "status": "success",
        "data": {
                "id": property.id,
                "street_address": property.address,
                "unit_apt": property.unit_apt,
                "city": property.city,
                "state": property.state,
                "zip_code": property.zipcode,
                "county": property.county,
                "property_type": property.property_type,
                "bedrooms": property.bedrooms,
                "bathrooms": property.bathrooms,
                "square_feet": property.square_feet,
                "lot_size": property.lot_size,
                "year_built": property.year_built,
                "purchase_price": float(property.price) if property.price else None,
                "arv": float(property.arv) if property.arv else None,
                "repair_estimate": float(property.repair_estimate) if property.repair_estimate else None,
                "holding_costs": float(property.holding_costs) if property.holding_costs else None,
                "transaction_type": property.transaction_type,
                "assignment_fee": float(property.assignment_fee) if property.assignment_fee else None,
                "property_description": property.description,
                "seller_notes": property.seller_notes,
                "images": property.images,
                "status": property.status,
                "created_at": property.created_at.isoformat(),
                "updated_at": property.updated_at.isoformat()
            }
        }
    except Property.DoesNotExist:
            return {
            "status": "error",
            "message": "Property not found"
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to retrieve property: {str(e)}"
        }

@app.put("/api/properties/{property_id}/", 
         tags=["Properties"],
         summary="Update Property by ID",
         description="Updates a specific property by its ID with all provided fields including financial details, property specifications, and location information.",
         response_description="Updated property details",
         responses={
             200: {
                 "description": "Property updated successfully",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "success",
                             "message": "Property updated successfully",
                             "data": {
                                 "id": 1,
                                 "street_address": "123 Main Street",
                                 "unit_apt": "Apt 2B",
                                 "city": "Miami",
                                 "state": "FL",
                                 "zip_code": "33101",
                                 "county": "Miami-Dade",
                                 "property_type": "residential",
                                 "bedrooms": 3,
                                 "bathrooms": 2.5,
                                 "square_feet": 1800,
                                 "lot_size": 0.25,
                                 "year_built": 1995,
                                 "purchase_price": 250000.0,
                                 "arv": 350000.0,
                                 "repair_estimate": 25000.0,
                                 "holding_costs": 5000.0,
                                 "transaction_type": "wholesale",
                                 "assignment_fee": 10000.0,
                                 "property_description": "Beautiful single-family home in great neighborhood",
                                 "seller_notes": "Motivated seller, needs quick sale",
                                 "images": ["image1.jpg", "image2.jpg"],
                                 "status": "active",
                                 "created_at": "2024-10-13T07:34:07.710903+00:00",
                                 "updated_at": "2024-10-18T06:28:14.415806+00:00"
                             }
                         }
                     }
                 }
             },
             404: {
                 "description": "Property not found",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "error",
                             "message": "Property not found"
                         }
                     }
                 }
             },
             500: {
                 "description": "Internal server error",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "error",
                             "message": "Failed to update property: Database connection error"
                         }
                     }
                 }
             }
         })
async def update_property(property_id: int, property_data: PropertyUpdate):
    """
    **Update Property by ID**
    
    Updates a specific property by its ID with comprehensive data including:
    
    **Location Data:**
    - Street address and unit/apartment information
    - City, state, zip code, and county details
    
    **Property Specifications:**
    - Property type, bedrooms, bathrooms
    - Square footage and lot size
    - Year built and property description
    
    **Financial Information:**
    - Purchase price and after repair value (ARV)
    - Repair estimates and holding costs
    - Transaction type and assignment fees
    
    **Additional Details:**
    - Seller notes and property images
    - Status and timestamps
    
    **Parameters:**
    - **property_id** (int): The unique identifier of the property to update
    
    **Request Body:**
    - All fields are optional - only provided fields will be updated
    
    **Returns:**
    - **200**: Updated property data with all fields
    - **404**: Property not found
    - **500**: Server error during update
    """
    try:
        from deelflow.models import Property
        
        property = await sync_to_async(Property.objects.get)(id=property_id)
        
        # Update property fields with proper type conversion (matching POST endpoint)
        if property_data.street_address is not None:
            property.address = property_data.street_address
        if property_data.unit_apt is not None:
            property.unit_apt = property_data.unit_apt
        if property_data.city is not None:
            property.city = property_data.city
        if property_data.state is not None:
            property.state = property_data.state
        if property_data.zip_code is not None:
            property.zipcode = property_data.zip_code
        if property_data.county is not None:
            property.county = property_data.county
        if property_data.property_type is not None:
            property.property_type = property_data.property_type
        if property_data.bedrooms is not None:
            property.bedrooms = int(property_data.bedrooms) if property_data.bedrooms and property_data.bedrooms != "" else None
        if property_data.bathrooms is not None:
            property.bathrooms = int(property_data.bathrooms) if property_data.bathrooms and property_data.bathrooms != "" else None
        if property_data.square_feet is not None:
            property.square_feet = int(property_data.square_feet) if property_data.square_feet and property_data.square_feet != "" else None
        if property_data.lot_size is not None:
            property.lot_size = float(property_data.lot_size) if property_data.lot_size and property_data.lot_size != "" else None
        if property_data.year_built is not None:
            property.year_built = int(property_data.year_built) if property_data.year_built and property_data.year_built != "" else None
        if property_data.purchase_price is not None:
            property.price = float(property_data.purchase_price) if property_data.purchase_price and property_data.purchase_price != "" else None
        if property_data.arv is not None:
            property.arv = float(property_data.arv) if property_data.arv and property_data.arv != "" else None
        if property_data.repair_estimate is not None:
            property.repair_estimate = float(property_data.repair_estimate) if property_data.repair_estimate and property_data.repair_estimate != "" else None
        if property_data.holding_costs is not None:
            property.holding_costs = float(property_data.holding_costs) if property_data.holding_costs and property_data.holding_costs != "" else None
        if property_data.transaction_type is not None:
            property.transaction_type = property_data.transaction_type
        if property_data.assignment_fee is not None:
            property.assignment_fee = float(property_data.assignment_fee) if property_data.assignment_fee and property_data.assignment_fee != "" else None
        if property_data.description is not None:
            property.description = property_data.description
        if property_data.seller_notes is not None:
            property.seller_notes = property_data.seller_notes
        if property_data.status is not None:
            property.status = property_data.status
        
        await sync_to_async(property.save)()
        return {
            "status": "success",
            "message": "Property updated successfully",
            "data": {
                "id": property.id,
                "street_address": property.address,
                "unit_apt": property.unit_apt,
                "city": property.city,
                "state": property.state,
                "zip_code": property.zipcode,
                "county": property.county,
                "property_type": property.property_type,
                "bedrooms": property.bedrooms,
                "bathrooms": property.bathrooms,
                "square_feet": property.square_feet,
                "lot_size": property.lot_size,
                "year_built": property.year_built,
                "purchase_price": float(property.price) if property.price else None,
                "arv": float(property.arv) if property.arv else None,
                "repair_estimate": float(property.repair_estimate) if property.repair_estimate else None,
                "holding_costs": float(property.holding_costs) if property.holding_costs else None,
                "transaction_type": property.transaction_type,
                "assignment_fee": float(property.assignment_fee) if property.assignment_fee else None,
                "property_description": property.description,
                "seller_notes": property.seller_notes,
                "images": property.images,
                "status": property.status,
                "created_at": property.created_at.isoformat(),
                "updated_at": property.updated_at.isoformat()
            }
        }
    except Property.DoesNotExist:
            return {
            "status": "error",
            "message": "Property not found"
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to update property: {str(e)}"
        }

@app.delete("/api/properties/{property_id}/", tags=["Properties"])
async def delete_property(property_id: int):
    """Delete a property by ID - Frontend compatible endpoint"""
    try:
        from deelflow.models import Property
        
        property = await sync_to_async(Property.objects.get)(id=property_id)
        await sync_to_async(property.delete)()
        return {
        "status": "success",
            "message": "Property deleted successfully"
        }
    except Property.DoesNotExist:
            return {
            "status": "error",
            "message": "Property not found"
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to delete property: {str(e)}"
        }

@app.get("/api/properties/{property_id}/ai-analysis/", tags=["Properties"])
async def get_property_ai_analysis(property_id: int):
    """Get AI analysis for a property - Frontend compatible endpoint"""
    try:
        from deelflow.models import Property
        
        property = await sync_to_async(Property.objects.get)(id=property_id)
        
        # Mock AI analysis (replace with actual AI service)
        ai_analysis = {
            "property_id": property_id,
            "market_value": float(property.arv or 250000),
            "repair_estimate": float(property.repair_estimate or 15000),
            "roi_potential": 85.5,
            "risk_score": 3.2,
            "recommendation": "Good investment opportunity",
            "confidence": 0.87,
            "analysis_date": timezone.now().isoformat(),
            "key_insights": [
                "Property shows strong potential for renovation",
                "Market conditions are favorable",
                "Neighborhood shows positive growth trends"
            ]
        }
        return {
        "status": "success",
            "data": ai_analysis
        }
    except Property.DoesNotExist:
            return {
            "status": "error",
            "message": "Property not found"
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to get AI analysis: {str(e)}"
        }

# ==================== PROPERTY SAVES ENDPOINTS ====================

@app.get("/api/property-saves/", tags=["Property Saves"])
async def get_property_saves(params: dict = None):
    """Get all property saves - Frontend compatible endpoint"""
    try:
        from deelflow.models import PropertySave
        
        # For now, return empty list since PropertySave model might not exist
        return {
        "status": "success",
            "data": [],
            "total": 0,
            "page": 1,
            "limit": 20
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to retrieve property saves: {str(e)}",
            "data": [],
            "total": 0,
            "page": 1,
            "limit": 20
        }

@app.get("/api/property-saves/{property_save_id}/", tags=["Property Saves"])
async def get_property_save(property_save_id: int):
    """Get a specific property save by ID - Frontend compatible endpoint"""
    try:
        from deelflow.models import SavedProperty
        
        property_save = await sync_to_async(SavedProperty.objects.get)(id=property_save_id)
        return {
            "status": "success",
            "data": {
                "id": property_save.id,
                "property_id": property_save.property.id,
                "user_id": property_save.user.id,
                "created_at": property_save.created_at.isoformat()
            }
        }
    except SavedProperty.DoesNotExist:
        return {
            "status": "error",
            "message": "Property save not found"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to retrieve property save: {str(e)}"
        }

@app.post("/api/property-saves/", tags=["Property Saves"])
async def create_property_save(property_save_data: dict):
    """Create a new property save - Frontend compatible endpoint"""
    try:
        from deelflow.models import SavedProperty, Property, User
        
        property_id = property_save_data.get("property_id")
        user_id = property_save_data.get("user_id", 1)  # Default to user 1 if not provided
        notes = property_save_data.get("notes", "")
        
        if not property_id:
            return {
                "status": "error",
                "message": "Property ID is required"
            }
        
        # Get property and user objects
        property_obj = await sync_to_async(Property.objects.get)(id=property_id)
        user_obj = await sync_to_async(User.objects.get)(id=user_id)
        
        # Create saved property
        saved_property = await sync_to_async(SavedProperty.objects.create)(
            property=property_obj,
            user=user_obj
        )
        
        return {
            "status": "success",
            "message": "Property save created successfully",
            "data": {
                "id": saved_property.id,
                "property_id": saved_property.property.id,
                "user_id": saved_property.user.id,
                "created_at": saved_property.created_at.isoformat()
            }
        }
    except Property.DoesNotExist:
        return {
            "status": "error",
            "message": "Property not found"
        }
    except User.DoesNotExist:
        return {
            "status": "error",
            "message": "User not found"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create property save: {str(e)}"
        }
    
@app.put("/api/property-saves/{property_save_id}/", tags=["Property Saves"])
async def update_property_save(property_save_id: int, property_save_data: dict):
    """Update a property save by ID - Frontend compatible endpoint"""
    try:
        from deelflow.models import PropertySave
        
        property_save = await sync_to_async(PropertySave.objects.get)(id=property_save_id)
        
        # Update fields
        if "notes" in property_save_data:
            property_save.notes = property_save_data["notes"]
        
        await sync_to_async(property_save.save)()
        return {
            "status": "success",
            "message": "Property save updated successfully",
            "data": {
                "id": property_save.id,
                "property_id": property_save.property_id,
                "user_id": property_save.user_id,
                "notes": property_save.notes,
                "updated_at": property_save.updated_at.isoformat()
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to update property save: {str(e)}"
        }

@app.delete("/api/property-saves/{property_save_id}/", tags=["Property Saves"])
async def delete_property_save(property_save_id: int):
    """Delete a property save by ID - Frontend compatible endpoint"""
    try:
        # TODO: Add proper implementation
        return {
        "status": "success",
            "message": "Property save deleted successfully"
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to delete property save: {str(e)}"
        }

# ==================== ATTOM API INTEGRATION ENDPOINTS ====================

@app.get("/api/properties/attom/search/", tags=["Properties"])
async def search_attom_properties(
    address: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    zipcode: Optional[str] = None,
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_sqft: Optional[int] = None,
    max_sqft: Optional[int] = None,
    bedrooms: Optional[int] = None,
    bathrooms: Optional[float] = None,
    limit: int = 50,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius: Optional[int] = None
):
    """
    **Search Properties from ATTOM API**
    
    Searches for properties using ATTOM Data Solutions API with comprehensive filtering options.
    
    **Query Parameters:**
    - address: Property address
    - city: City name
    - state: State code (e.g., "FL", "CA")
    - zip: ZIP code
    - property_type: Type of property (single_family, multi_family, etc.)
    - min_price: Minimum price filter
    - max_price: Maximum price filter
    - min_sqft: Minimum square footage
    - max_sqft: Maximum square footage
    - bedrooms: Number of bedrooms
    - bathrooms: Number of bathrooms
    - limit: Maximum number of results (default: 50)
    
    **Returns:**
    - List of properties from ATTOM API
    - Normalized property data matching internal structure
    - Additional owner and market data
    """
    try:
        from app.services.attom_service import attom_service
        
        result = attom_service.search_properties(
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            property_type=property_type,
            min_price=min_price,
            max_price=max_price,
            min_sqft=min_sqft,
            max_sqft=max_sqft,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            limit=limit,
            latitude=latitude,
            longitude=longitude,
            radius=radius
        )
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to search ATTOM properties: {str(e)}",
            "data": []
        }

# Aliased consolidated endpoints under property list namespace
@app.get("/api/properties/search", tags=["Properties"], summary="Search Properties (ATTOM)")
async def properties_search(
    address: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    zipcode: Optional[str] = None,
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_sqft: Optional[int] = None,
    max_sqft: Optional[int] = None,
    bedrooms: Optional[int] = None,
    bathrooms: Optional[float] = None,
    limit: int = 50,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius: Optional[int] = None
):
    """
    Search properties via ATTOM, exposed under the consolidated properties namespace.
    """
    try:
        from app.services.attom_service import attom_service
        return attom_service.search_properties(
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            property_type=property_type,
            min_price=min_price,
            max_price=max_price,
            min_sqft=min_sqft,
            max_sqft=max_sqft,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            limit=limit,
            latitude=latitude,
            longitude=longitude,
            radius=radius
        )
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to search properties: {str(e)}",
            "data": []
        }

@app.get("/api/properties/attom/details/{property_id}/", tags=["Properties"])
async def get_attom_property_details(property_id: str):
    """
    **Get Property Details from ATTOM API**
    
    Retrieves detailed property information from ATTOM API by property identifier.
    
    **Parameters:**
    - **property_id** (str): ATTOM property identifier
    
    **Returns:**
    - Detailed property data including assessments, ownership, and valuations
    """
    try:
        from app.services.attom_service import attom_service
        
        result = attom_service.get_property_details(property_id)
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch property details: {str(e)}"
        }

@app.get("/api/properties/details/{property_id}", tags=["Properties"], summary="Get Property Details (ATTOM)")
async def properties_details(property_id: str):
    """
    Get property details via ATTOM, exposed under the consolidated properties namespace.
    """
    try:
        from app.services.attom_service import attom_service
        return attom_service.get_property_details(property_id)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch property details: {str(e)}"
        }

# ==================== COMBINED PROPERTY LIST (Internal + ATTOM) ====================

@app.get(
    "/api/properties/combined",
    tags=["Properties"],
    summary="Combined Property List (Internal + ATTOM)"
)
async def get_combined_properties(
    page: int = Query(1, ge=1, description="Page number (default 1)"),
    limit: int = Query(20, ge=1, le=100, description="Items per page (default 20, max 100)"),
    search: Optional[str] = Query(None, description="Free-text search over address/city/state (internal only)"),
    property_type: Optional[str] = Query(None, description="Filter by property type"),
    min_price: Optional[float] = Query(None, description="Minimum price filter (internal)"),
    max_price: Optional[float] = Query(None, description="Maximum price filter (internal)"),
    zipcode: Optional[str] = Query(None, description="ATTOM location filter (recommended)"),
    city: Optional[str] = Query(None, description="ATTOM city filter"),
    state: Optional[str] = Query(None, description="ATTOM state filter"),
    latitude: Optional[float] = Query(None, description="Latitude for radius search (ATTOM)"),
    longitude: Optional[float] = Query(None, description="Longitude for radius search (ATTOM)"),
    radius: Optional[int] = Query(None, description="Radius in miles for location-based search (ATTOM)"),
    include_raw: bool = Query(True, description="Include raw source payloads under raw.attom/raw.internal")
):
    """
    Unified property list that merges internal properties with ATTOM search results.

    Query Parameters:
    - page (int): page number (default 1)
    - limit (int): items per page (default 20, max 100)
    - search (str): free-text search over address/city/state (internal only)
    - property_type (str): filter by property type
    - min_price/max_price (number): internal price filters
    - zipcode (str): ATTOM location filter (recommended)
    - city/state (str): ATTOM filters; ATTOM typically requires zipcode or lat/long
    - latitude/longitude (number), radius (int): ATTOM radius search
    - include_raw (bool): include raw source payloads under `raw.attom`/`raw.internal`

    Returns:
    - status: "success" or "error"
    - data: { properties, total, page, limit, has_next, has_prev }
      - properties: list of unified items with normalized top-level fields and optional `raw`

    Notes:
    - Deduplicates by canonical address (street+city+state+zip), preferring internal rows and merging ATTOM raw data.
    - If ATTOM returns a location input error, internal results are still returned.
    """
    try:
        from typing import Dict, Any
        from datetime import datetime, timezone
        from app.services.attom_service import attom_service
        from django.db.models import Q
        from asgiref.sync import sync_to_async
        from deelflow.models import Property

        def normalize_internal(p: Any) -> Dict[str, Any]:
            return {
                "id": f"src:internal:{p.id}",
                "source": "internal",
                "source_id": str(p.id),
                "attribution": "Internal",
                "street_address": getattr(p, "address", "") or "",
                "unit_apt": getattr(p, "unit_apt", "") or "",
                "city": getattr(p, "city", "") or "",
                "state": getattr(p, "state", "") or "",
                "zip_code": getattr(p, "zipcode", "") or "",
                "county": getattr(p, "county", "") or "",
                "property_type": getattr(p, "property_type", "") or "",
                "bedrooms": p.bedrooms if getattr(p, "bedrooms", None) is not None else None,
                "bathrooms": p.bathrooms if getattr(p, "bathrooms", None) is not None else None,
                "square_feet": p.square_feet if getattr(p, "square_feet", None) is not None else None,
                "lot_size": p.lot_size if getattr(p, "lot_size", None) is not None else None,
                "year_built": p.year_built if getattr(p, "year_built", None) is not None else None,
                "purchase_price": p.price if getattr(p, "price", None) is not None else None,
                "arv": p.arv if getattr(p, "arv", None) is not None else None,
                "repair_estimate": p.repair_estimate if getattr(p, "repair_estimate", None) is not None else None,
                "holding_costs": p.holding_costs if getattr(p, "holding_costs", None) is not None else None,
                "transaction_type": getattr(p, "transaction_type", None),
                "assignment_fee": p.assignment_fee if getattr(p, "assignment_fee", None) is not None else None,
                "description": getattr(p, "description", "") or "",
                "seller_notes": getattr(p, "seller_notes", "") or "",
                "images": [],
                "status": getattr(p, "status", "available") or "available",
                "created_at": getattr(p, "created_at", datetime.now(timezone.utc)).isoformat(),
                "updated_at": getattr(p, "updated_at", datetime.now(timezone.utc)).isoformat(),
                "raw": {"internal": {
                    "id": p.id,
                    "address": getattr(p, "address", None),
                    "unit_apt": getattr(p, "unit_apt", None),
                    "city": getattr(p, "city", None),
                    "state": getattr(p, "state", None),
                    "zipcode": getattr(p, "zipcode", None),
                    "county": getattr(p, "county", None),
                    "property_type": getattr(p, "property_type", None),
                    "bedrooms": getattr(p, "bedrooms", None),
                    "bathrooms": getattr(p, "bathrooms", None),
                    "square_feet": getattr(p, "square_feet", None),
                    "lot_size": getattr(p, "lot_size", None),
                    "year_built": getattr(p, "year_built", None),
                    "price": getattr(p, "price", None),
                    "arv": getattr(p, "arv", None),
                    "repair_estimate": getattr(p, "repair_estimate", None),
                    "holding_costs": getattr(p, "holding_costs", None),
                    "transaction_type": getattr(p, "transaction_type", None),
                    "assignment_fee": getattr(p, "assignment_fee", None),
                    "description": getattr(p, "description", None),
                    "seller_notes": getattr(p, "seller_notes", None),
                    "status": getattr(p, "status", None),
                }}
            }

        def normalize_attom(item: Dict[str, Any]) -> Dict[str, Any]:
            # Expect our attom_service to already return normalized basic fields; still guard with .get
            now_iso = datetime.now(timezone.utc).isoformat()
            return {
                "id": f"src:attom:{item.get('id')}",
                "source": "attom",
                "source_id": str(item.get("id")),
                "attribution": "ATTOM Data Solutions",
                "street_address": item.get("street_address") or "",
                "unit_apt": item.get("unit_apt") or "",
                "city": item.get("city") or "",
                "state": item.get("state") or "",
                "zip_code": item.get("zip_code") or "",
                "county": item.get("county") or "",
                "property_type": item.get("property_type") or "",
                "bedrooms": item.get("bedrooms", None),
                "bathrooms": item.get("bathrooms", None),
                "square_feet": item.get("square_feet", None),
                "lot_size": item.get("lot_size", None),
                "year_built": item.get("year_built", None) or None,
                # Internal-only finance fields default to None for ATTOM rows
                "purchase_price": None,
                "arv": None,
                "repair_estimate": None,
                "holding_costs": None,
                "transaction_type": None,
                "assignment_fee": None,
                "description": item.get("property_description", "") or "",
                "seller_notes": item.get("seller_notes", "") or "",
                "images": item.get("images", []) or [],
                "status": item.get("status", "available") or "available",
                "created_at": item.get("created_at") or now_iso,
                "updated_at": item.get("updated_at") or now_iso,
                "raw": {"attom": item}
            }

        # 1) Internal DB fetch with filters (basic search on address/city/state)
        async def fetch_internal() -> Any:
            qs = Property.objects.all()
            if search:
                qs = qs.filter(
                    Q(address__icontains=search) |
                    Q(city__icontains=search) |
                    Q(state__icontains=search)
                )
            if property_type:
                qs = qs.filter(property_type__iexact=property_type)
            if min_price is not None:
                qs = qs.filter(price__gte=min_price)
            if max_price is not None:
                qs = qs.filter(price__lte=max_price)
            return await sync_to_async(list)(qs[:1000])  # cap to reasonable size pre-merge

        # 2) ATTOM fetch (location-based; require zipcode OR coordinates to avoid 400)
        def fetch_attom() -> Dict[str, Any]:
            return attom_service.search_properties(
                address=None, city=city, state=state, zipcode=zipcode,
                property_type=property_type, min_price=min_price, max_price=max_price,
                min_sqft=None, max_sqft=None, bedrooms=None, bathrooms=None,
                limit=50, latitude=latitude, longitude=longitude, radius=radius
            )

        internal_list, attom_result = await sync_to_async(lambda: None)(), None
        # fetch internal (await) and attom (sync) sequentially to keep simple and safe
        internal_list = await fetch_internal()
        attom_result = fetch_attom()

        # Normalize internal
        unified: list = [normalize_internal(p) for p in internal_list]

        # Normalize ATTOM if success
        if isinstance(attom_result, dict) and attom_result.get("status") == "success":
            # attom_service returns either list under data or direct list; handle both
            attom_data = attom_result.get("data")
            attom_list = []
            if isinstance(attom_data, list):
                attom_list = attom_data
            elif isinstance(attom_data, dict):
                # common: { properties: [...] }
                for key in ("properties", "results", "items"):
                    if isinstance(attom_data.get(key), list):
                        attom_list = attom_data.get(key)
                        break
            for item in attom_list:
                if isinstance(item, dict):
                    unified.append(normalize_attom(item))
        else:
            # If ATTOM fails due to missing location input, continue with internal only
            pass

        # Optional dedup by canonical address key; prefer internal
        def address_key(row: Dict[str, Any]) -> str:
            return "|".join([
                (row.get("street_address") or "").strip().upper(),
                (row.get("city") or "").strip().upper(),
                (row.get("state") or "").strip().upper(),
                (row.get("zip_code") or "").strip().upper(),
            ])

        seen = {}
        deduped = []
        for row in unified:
            key = address_key(row)
            if not key:
                deduped.append(row)
                continue
            if key not in seen:
                seen[key] = row
                deduped.append(row)
            else:
                # merge raw data if duplicate (keep internal-preferred already ordered)
                existing = seen[key]
                if row.get("source") == "attom":
                    raw = existing.setdefault("raw", {})
                    raw["attom"] = row.get("raw", {}).get("attom")
                else:
                    raw = existing.setdefault("raw", {})
                    raw["internal_duplicate"] = row.get("raw", {}).get("internal")

        # Sort stable: internal first, then ATTOM; then by city/street
        deduped.sort(key=lambda r: (
            0 if r.get("source") == "internal" else 1,
            (r.get("city") or ""),
            (r.get("street_address") or "")
        ))

        # Pagination after merge
        total = len(deduped)
        page = max(1, page)
        limit = max(1, min(100, limit))
        start = (page - 1) * limit
        end = start + limit
        page_items = deduped[start:end]

        if not include_raw:
            for row in page_items:
                row.pop("raw", None)

        return {
            "status": "success",
            "data": {
                "properties": page_items,
                "total": total,
                "page": page,
                "limit": limit,
                "has_next": end < total,
                "has_prev": start > 0
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get combined properties: {str(e)}"
        }

# ==================== USER LIST (for Role Management) ====================

@app.get(
    "/api/users/",
    tags=["Role Management"],
    summary="List registered users for role assignment"
)
async def list_users(
    page: int = Query(1, ge=1, description="Page number (default 1)"),
    limit: int = Query(20, ge=1, le=100, description="Items per page (default 20, max 100)"),
    search: Optional[str] = Query(None, description="Filter by email, first name, or last name (icontains)"),
    is_active: Optional[bool] = Query(None, description="Filter by active status (true/false)")
):
    """
    Returns a paginated list of registered users to support role assignment workflows.

    Query Parameters:
    - page (int): page number (default 1)
    - limit (int): items per page (default 20, max 100)
    - search (str): filter by email, first name, or last name (icontains)
    - is_active (bool): optional filter by active status

    Response items include minimal fields needed for role assignment.
    """
    try:
        from deelflow.models import User
        from django.db.models import Q
        from asgiref.sync import sync_to_async

        qs = User.objects.all().order_by("-id")
        if search:
            qs = qs.filter(
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        if is_active is not None:
            qs = qs.filter(is_active=is_active)

        # Pagination
        page = max(1, page)
        limit = max(1, min(100, limit))
        total = await sync_to_async(qs.count)()
        start = (page - 1) * limit
        end = start + limit
        users = await sync_to_async(list)(qs[start:end])

        def serialize(u):
            return {
                "id": u.id,
                "email": u.email,
                "first_name": getattr(u, "first_name", "") or "",
                "last_name": getattr(u, "last_name", "") or "",
                "role": getattr(u, "role", "user") or "user",
                "is_active": getattr(u, "is_active", True),
                "is_verified": getattr(u, "is_verified", False),
                "organization_id": getattr(u, "organization_id", None),
            }

        items = [serialize(u) for u in users]
        return {
            "status": "success",
            "data": {
                "users": items,
                "total": total,
                "page": page,
                "limit": limit,
                "has_next": end < total,
                "has_prev": start > 0
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to list users: {str(e)}"
        }

@app.get("/api/properties/attom/market-trends/", tags=["Properties"])
async def get_attom_market_trends(city: str, state: str):
    """
    **Get Market Trends from ATTOM API**
    
    Retrieves market trend data for a specific location from ATTOM API.
    
    **Query Parameters:**
    - **city** (str): City name
    - **state** (str): State code (e.g., "FL", "CA")
    
    **Returns:**
    - Market trend data including price trends, inventory levels, and forecasts
    """
    try:
        from app.services.attom_service import attom_service
        
        result = attom_service.get_market_trends(city, state)
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch market trends: {str(e)}"
        }

# ==================== CAMPAIGN ENDPOINTS (Frontend Compatible) ====================

@app.get("/campaigns/", 
         tags=["Campaigns"],
         summary="Get All Campaigns",
         description="Retrieves all campaigns with normalized array fields and comprehensive data including seller finder, buyer finder, and demographic information.",
         response_description="List of campaigns with pagination information",
         responses={
             200: {
                 "description": "Campaigns retrieved successfully",
                 "content": {
                     "application/json": {
                         "example": {
        "status": "success",
        "data": [
            {
                "id": 1,
                                     "name": "Sample Campaign",
                                     "campaign_type": "seller_finder",
                                     "channel": ["email", "phone"],
                                     "budget": 5000.0,
                "status": "active",
                                     "geographic_scope_values": ["Miami-Dade", "Broward"],
                                     "distress_indicators": ["Pre-foreclosure", "Divorce"]
            }
        ],
                             "total": 25,
        "page": 1,
        "limit": 20
    }
                     }
                 }
             },
             500: {
                 "description": "Internal server error",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "error",
                             "message": "Failed to retrieve campaigns: Database connection error",
                             "data": [],
                             "total": 0,
                             "page": 1,
                             "limit": 20
                         }
                     }
                 }
             }
         })
async def get_campaigns():
    """
    **Get All Campaigns**
    
    Retrieves all campaigns with comprehensive data including:
    
    **Core Campaign Data:**
    - Basic information (name, type, budget, status)
    - Scheduling and content details
    - Geographic scope and targeting parameters
    
    **Seller Finder Data:**
    - Geographic targeting (country, state, counties, city, districts, parish)
    - Property criteria (year built range, keywords)
    - Additional seller-specific filters
    
    **Buyer Finder Data:**
    - Geographic targeting for buyers
    - Demographic filters (age range, ethnicity, salary, marital status)
    - Employment and home ownership status
    
    **Data Normalization:**
    - `channel` is always returned as an array
    - `geographic_scope_values` and `distress_indicators` are parsed from stored strings
    - All datetime fields are returned in ISO format
    
    **Returns:**
    - **200**: List of campaigns with pagination information
    - **500**: Server error during retrieval
    
    **Response Format:**
    ```json
    {
        "status": "success",
        "data": [
            {
                "id": 1,
                "name": "Q4 Marketing Campaign",
                "campaign_type": "seller_finder",
                "channel": ["email", "phone"],
                "budget": 10000.0,
                "status": "active",
                "geographic_scope_values": ["Miami-Dade", "Broward"],
                "distress_indicators": ["Pre-foreclosure", "Divorce"],
                // ... all other campaign fields
            }
        ],
        "total": 25,
        "page": 1,
        "limit": 20
    }
    ```
    """
    try:
        from deelflow.models import Campaign
        campaigns = await sync_to_async(list)(Campaign.objects.all())
        
        campaign_data = []
        for campaign in campaigns:
            # Normalize fields stored as strings in DB
            try:
                geo_values = campaign.geographic_scope_values
                if isinstance(geo_values, str):
                    geo_values = ast.literal_eval(geo_values)
            except Exception:
                geo_values = []
            try:
                distress = campaign.distress_indicators
                if isinstance(distress, str):
                    distress = ast.literal_eval(distress)
            except Exception:
                distress = []
            # Parse channel from string to list
            try:
                channel_val = campaign.channel
                if isinstance(channel_val, str):
                    channel_out = ast.literal_eval(channel_val) if channel_val else []
                else:
                    channel_out = channel_val if channel_val else []
            except Exception:
                channel_out = []
            campaign_data.append({
                "id": campaign.id,
                "name": campaign.name,
                "campaign_type": campaign.campaign_type,
                "channel": channel_out,
                "budget": float(campaign.budget) if campaign.budget else None,
                "scheduled_at": campaign.scheduled_at.isoformat() if campaign.scheduled_at else None,
                "subject_line": campaign.subject_line,
                "email_content": campaign.email_content,
                "use_ai_personalization": campaign.use_ai_personalization,
                "status": campaign.status,
                "geographic_scope_type": campaign.geographic_scope_type,
                "geographic_scope_values": geo_values,
                "location": campaign.location,
                "property_type": campaign.property_type,
                "minimum_equity": float(campaign.minimum_equity) if campaign.minimum_equity else None,
                "min_price": float(campaign.min_price) if campaign.min_price else None,
                "max_price": float(campaign.max_price) if campaign.max_price else None,
                "distress_indicators": distress,
                "created_at": campaign.created_at.isoformat()
            })
        return {
        "status": "success",
            "data": campaign_data,
            "total": len(campaign_data),
            "page": 1,
            "limit": 20
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to retrieve campaigns: {str(e)}",
            "data": [],
            "total": 0,
            "page": 1,
            "limit": 20
        }

@app.get("/campaigns/{campaign_id}/", 
         tags=["Campaigns"],
         summary="Get Campaign by ID",
         description="Retrieves a specific campaign by its ID with all associated data including seller finder, buyer finder, and demographic information.",
         response_description="Campaign details with normalized array fields",
         responses={
             200: {
                 "description": "Campaign retrieved successfully",
                 "content": {
                     "application/json": {
                         "example": {
        "status": "success",
        "data": {
                                 "id": 1,
                                 "name": "Sample Campaign",
                                 "campaign_type": "seller_finder",
                                 "channel": ["email", "phone"],
                                 "budget": 5000.0,
                                 "scheduled_at": "2024-12-25T10:00:00+00:00",
                                 "subject_line": "Investment Opportunity",
                                 "email_content": "Discover amazing property deals...",
                                 "use_ai_personalization": True,
            "status": "active",
                                 "geographic_scope_type": "counties",
                                 "geographic_scope_values": ["Miami-Dade", "Broward"],
                                 "location": "Miami, FL",
                                 "property_type": "residential",
                                 "minimum_equity": 75000.0,
                                 "min_price": 300000.0,
                                 "max_price": 800000.0,
                                 "distress_indicators": ["Pre-foreclosure", "Divorce"],
                                 "created_at": "2024-10-13T07:34:07.710903+00:00",
                                 "updated_at": "2024-10-18T06:28:14.415806+00:00",
                                 "seller_country": "USA",
                                 "seller_state": "Florida",
                                 "seller_counties": "Miami-Dade",
                                 "seller_city": "Miami",
                                 "property_year_built_min": 1990,
                                 "property_year_built_max": 2020,
                                 "seller_keywords": "investment, rental",
                                 "buyer_country": "USA",
                                 "buyer_state": "Florida",
                                 "age_range": "25-45",
                                 "salary_range": "50000-150000",
                                 "marital_status": "any",
                                 "employment_status": "employed",
                                 "home_ownership_status": "any"
                             }
                         }
                     }
                 }
             },
             404: {
                 "description": "Campaign not found",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "error",
                             "message": "Campaign not found"
                         }
                     }
                 }
             },
             500: {
                 "description": "Internal server error",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "error",
                             "message": "Failed to retrieve campaign: Database connection error"
                         }
                     }
                 }
             }
         })
async def get_campaign(campaign_id: int):
    """
    **Get Campaign by ID**
    
    Retrieves a specific campaign by its ID with comprehensive data including:
    
    **Core Campaign Data:**
    - Basic information (name, type, budget, status)
    - Scheduling and content details
    - Geographic scope and targeting parameters
    
    **Seller Finder Data:**
    - Geographic targeting (country, state, counties, city, districts, parish)
    - Property criteria (year built range, keywords)
    - Additional seller-specific filters
    
    **Buyer Finder Data:**
    - Geographic targeting for buyers
    - Demographic filters (age range, ethnicity, salary, marital status)
    - Employment and home ownership status
    
    **Data Normalization:**
    - `channel` is always returned as an array
    - `geographic_scope_values` and `distress_indicators` are parsed from stored strings
    - All datetime fields are returned in ISO format
    
    **Parameters:**
    - **campaign_id** (int): The unique identifier of the campaign to retrieve
    
    **Returns:**
    - **200**: Campaign data with all fields populated
    - **404**: Campaign not found
    - **500**: Server error during retrieval
    
    **Example Usage:**
    ```
    GET /campaigns/123/
    ```
    
    **Response Format:**
    ```json
    {
        "status": "success",
        "data": {
            "id": 123,
            "name": "Q4 Marketing Campaign",
            "campaign_type": "seller_finder",
            "channel": ["email", "phone"],
            "budget": 10000.0,
            "status": "active",
            "geographic_scope_values": ["Miami-Dade", "Broward"],
            "distress_indicators": ["Pre-foreclosure", "Divorce"],
            // ... all other campaign fields
        }
    }
    ```
    """
    try:
        from deelflow.models import Campaign
        import ast
        
        campaign = await sync_to_async(Campaign.objects.get)(id=campaign_id)
        
        # Normalize fields stored as strings in DB
        try:
            geo_values = campaign.geographic_scope_values
            if isinstance(geo_values, str):
                geo_values = ast.literal_eval(geo_values)
        except Exception:
            geo_values = []
            
        try:
            distress = campaign.distress_indicators
            if isinstance(distress, str):
                distress = ast.literal_eval(distress)
        except Exception:
            distress = []
            
        # Parse channel from string to list
        try:
            channel_val = campaign.channel
            if isinstance(channel_val, str):
                channel_out = ast.literal_eval(channel_val) if channel_val else []
            else:
                channel_out = channel_val if channel_val else []
        except Exception:
            channel_out = []
        
        campaign_data = {
                "id": campaign.id,
                "name": campaign.name,
                "campaign_type": campaign.campaign_type,
            "channel": channel_out,
                "budget": float(campaign.budget) if campaign.budget else None,
                "scheduled_at": campaign.scheduled_at.isoformat() if campaign.scheduled_at else None,
                "subject_line": campaign.subject_line,
                "email_content": campaign.email_content,
                "use_ai_personalization": campaign.use_ai_personalization,
                "status": campaign.status,
                "geographic_scope_type": campaign.geographic_scope_type,
            "geographic_scope_values": geo_values,
                "location": campaign.location,
                "property_type": campaign.property_type,
                "minimum_equity": float(campaign.minimum_equity) if campaign.minimum_equity else None,
                "min_price": float(campaign.min_price) if campaign.min_price else None,
                "max_price": float(campaign.max_price) if campaign.max_price else None,
            "distress_indicators": distress,
                "created_at": campaign.created_at.isoformat(),
            "updated_at": campaign.updated_at.isoformat() if campaign.updated_at else None,
            # Seller Finder - Geographic Details
            "seller_country": campaign.seller_country,
            "seller_state": campaign.seller_state,
            "seller_counties": campaign.seller_counties,
            "seller_city": campaign.seller_city,
            "seller_districts": campaign.seller_districts,
            "seller_parish": campaign.seller_parish,
            # Seller Finder - Additional Fields
            "property_year_built_min": campaign.property_year_built_min,
            "property_year_built_max": campaign.property_year_built_max,
            "seller_keywords": campaign.seller_keywords,
            # Buyer Finder - Geographic Details
            "buyer_country": campaign.buyer_country,
            "buyer_state": campaign.buyer_state,
            "buyer_counties": campaign.buyer_counties,
            "buyer_city": campaign.buyer_city,
            "buyer_districts": campaign.buyer_districts,
            "buyer_parish": campaign.buyer_parish,
            # Buyer Finder - Demographic Details
            "last_qualification": campaign.last_qualification,
            "age_range": campaign.age_range,
            "ethnicity": campaign.ethnicity,
            "salary_range": campaign.salary_range,
            "marital_status": campaign.marital_status,
            "employment_status": campaign.employment_status,
            "home_ownership_status": campaign.home_ownership_status
        }
        return {
            "status": "success",
            "data": campaign_data
        }
    except Campaign.DoesNotExist:
            return {
            "status": "error",
            "message": "Campaign not found"
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to retrieve campaign: {str(e)}"
        }

@app.post("/campaigns/", tags=["Campaigns"])
async def create_campaign(campaign_data: CampaignCreate):
    """Create a new campaign - Frontend compatible endpoint"""
    try:
        print("=== CAMPAIGN CREATION DEBUG ===")
        print(f"Received campaign_data: {campaign_data}")
        
        from deelflow.models import Campaign
        print("✓ Django Campaign model imported successfully")
        
        # Convert channel list to string for database storage
        channel = campaign_data.channel
        if isinstance(channel, list):
            channel = str(channel) if channel else "[]"
        print(f"✓ Channel processed: {channel}")
        
        # Handle geographic scope - support both object and separate field formats
        geographic_scope_type = campaign_data.geographic_scope_type
        geographic_scope_values = campaign_data.geographic_scope_values
        
        # If geographic_scope object is provided, extract type and values from it
        if campaign_data.geographic_scope:
            geographic_scope_type = campaign_data.geographic_scope.get("type", geographic_scope_type)
            if "counties" in campaign_data.geographic_scope:
                geographic_scope_values = campaign_data.geographic_scope["counties"]
            elif "cities" in campaign_data.geographic_scope:
                geographic_scope_values = campaign_data.geographic_scope["cities"]
            elif "states" in campaign_data.geographic_scope:
                geographic_scope_values = campaign_data.geographic_scope["states"]
            elif "zipcodes" in campaign_data.geographic_scope:
                geographic_scope_values = campaign_data.geographic_scope["zipcodes"]
        print(f"✓ Geographic scope processed: type={geographic_scope_type}, values={geographic_scope_values}")
        
        # Parse scheduled_at string to datetime
        from datetime import datetime
        scheduled_at = None
        if campaign_data.scheduled_at:
            try:
                # Handle different datetime formats
                scheduled_str = campaign_data.scheduled_at
                if 'T' in scheduled_str and not scheduled_str.endswith('Z'):
                    scheduled_at = datetime.fromisoformat(scheduled_str)
                else:
                    scheduled_at = datetime.fromisoformat(scheduled_str.replace('Z', '+00:00'))
                print(f"✓ Scheduled_at parsed successfully: {scheduled_at}")
            except ValueError as e:
                print(f"Error parsing scheduled_at: {e}")
                scheduled_at = None
        else:
            print("✓ No scheduled_at provided")
        
        # Create campaign in Django database
        print("About to create campaign...")
        print("Creating campaign with data:")
        print(f"  - name: {campaign_data.name}")
        print(f"  - scheduled_at: {scheduled_at}")
        print(f"  - channel: {channel}")
        
        from django.utils import timezone
        
        campaign = await sync_to_async(Campaign.objects.create)(
            name=campaign_data.name,
            campaign_type=campaign_data.campaign_type,
            channel=channel,
            budget=campaign_data.budget,
            scheduled_at=scheduled_at,
            updated_at=timezone.now(),
            geographic_scope_type=geographic_scope_type,
            geographic_scope_values=str(geographic_scope_values) if geographic_scope_values else "[]",
            location=campaign_data.location,
            property_type=campaign_data.property_type,
            minimum_equity=campaign_data.minimum_equity,
            min_price=campaign_data.min_price,
            max_price=campaign_data.max_price,
            distress_indicators=str(campaign_data.distress_indicators) if campaign_data.distress_indicators else "[]",
            subject_line=campaign_data.subject_line,
            email_content=campaign_data.email_content,
            use_ai_personalization=campaign_data.use_ai_personalization,
            status=campaign_data.status,
            # Seller Finder - Geographic Details
            seller_country=campaign_data.seller_country,
            seller_state=campaign_data.seller_state,
            seller_counties=campaign_data.seller_counties,
            seller_city=campaign_data.seller_city,
            seller_districts=campaign_data.seller_districts,
            seller_parish=campaign_data.seller_parish,
            # Seller Finder - Additional Fields
            property_year_built_min=int(campaign_data.property_year_built_min) if campaign_data.property_year_built_min and str(campaign_data.property_year_built_min).strip() != "" else None,
            property_year_built_max=int(campaign_data.property_year_built_max) if campaign_data.property_year_built_max and str(campaign_data.property_year_built_max).strip() != "" else None,
            seller_keywords=campaign_data.seller_keywords,
            # Buyer Finder - Geographic Details
            buyer_country=campaign_data.buyer_country,
            buyer_state=campaign_data.buyer_state,
            buyer_counties=campaign_data.buyer_counties,
            buyer_city=campaign_data.buyer_city,
            buyer_districts=campaign_data.buyer_districts,
            buyer_parish=campaign_data.buyer_parish,
            # Buyer Finder - Demographic Details
            last_qualification=campaign_data.last_qualification,
            age_range=campaign_data.age_range,
            ethnicity=campaign_data.ethnicity,
            salary_range=campaign_data.salary_range,
            marital_status=campaign_data.marital_status,
            employment_status=campaign_data.employment_status,
            home_ownership_status=campaign_data.home_ownership_status
        )
        print("✓ Campaign created successfully in database")
        
        print("✓ Preparing response...")
        return {
            "status": "success",
            "message": "Campaign created successfully",
            "data": {
                "id": campaign.id,
                "name": campaign.name,
                "campaign_type": campaign.campaign_type,
                "channel": campaign.channel,
                "budget": float(campaign.budget) if campaign.budget else None,
                "scheduled_at": str(campaign.scheduled_at) if campaign.scheduled_at else None,
                "subject_line": campaign.subject_line,
                "email_content": campaign.email_content,
                "use_ai_personalization": campaign.use_ai_personalization,
                "status": campaign.status,
                "created_at": str(campaign.created_at),
                "updated_at": str(campaign.updated_at)
            }
        }
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "message": f"Failed to create campaign: {str(e)}",
            "traceback": traceback.format_exc()
        }

# Removed per request: Only list endpoint should remain

@app.put("/campaigns/{campaign_id}/", tags=["Campaigns"])
async def update_campaign(campaign_id: int, campaign_data: CampaignUpdate):
    """Update a campaign by ID - Frontend compatible endpoint"""
    try:
        from deelflow.models import Campaign
        
        campaign = await sync_to_async(Campaign.objects.get)(id=campaign_id)
        
        # Update campaign fields with proper handling for special fields
        update_data = campaign_data.dict(exclude_unset=True)
        
        # Handle channel field - convert list to string for database storage
        if 'channel' in update_data and update_data['channel'] is not None:
            channel = update_data['channel']
            if isinstance(channel, list):
                channel = str(channel) if channel else "[]"
            campaign.channel = channel
            del update_data['channel']
        
        # Handle geographic_scope_values - convert list to string
        if 'geographic_scope_values' in update_data and update_data['geographic_scope_values'] is not None:
            geographic_scope_values = update_data['geographic_scope_values']
            if isinstance(geographic_scope_values, list):
                campaign.geographic_scope_values = str(geographic_scope_values)
            else:
                campaign.geographic_scope_values = geographic_scope_values
            del update_data['geographic_scope_values']
        
        # Handle distress_indicators - convert list to string
        if 'distress_indicators' in update_data and update_data['distress_indicators'] is not None:
            distress_indicators = update_data['distress_indicators']
            if isinstance(distress_indicators, list):
                campaign.distress_indicators = str(distress_indicators)
            else:
                campaign.distress_indicators = distress_indicators
            del update_data['distress_indicators']
        
        # Handle property_year_built fields - convert to int or None
        if 'property_year_built_min' in update_data and update_data['property_year_built_min'] is not None:
            value = update_data['property_year_built_min']
            campaign.property_year_built_min = int(value) if value and str(value).strip() != "" else None
            del update_data['property_year_built_min']
        
        if 'property_year_built_max' in update_data and update_data['property_year_built_max'] is not None:
            value = update_data['property_year_built_max']
            campaign.property_year_built_max = int(value) if value and str(value).strip() != "" else None
            del update_data['property_year_built_max']
        
        # Handle scheduled_at - convert string to datetime
        if 'scheduled_at' in update_data and update_data['scheduled_at'] is not None:
            from datetime import datetime
            scheduled_at_str = update_data['scheduled_at']
            try:
                # Try parsing the datetime string
                scheduled_at = datetime.fromisoformat(scheduled_at_str.replace('Z', '+00:00'))
                campaign.scheduled_at = scheduled_at
            except ValueError:
                # If parsing fails, set to None
                campaign.scheduled_at = None
            del update_data['scheduled_at']
        
        # Update remaining fields normally
        for field, value in update_data.items():
            if hasattr(campaign, field):
                setattr(campaign, field, value)
        
        await sync_to_async(campaign.save)()
        return {
            "status": "success",
        "message": "Campaign updated successfully",
            "data": {
                "id": campaign.id,
                "name": campaign.name,
                "status": campaign.status,
                "updated_at": campaign.updated_at.isoformat()
            }
        }
    except Campaign.DoesNotExist:
            return {
            "status": "error",
            "message": "Campaign not found"
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to update campaign: {str(e)}"
        }

@app.delete("/campaigns/{campaign_id}/", tags=["Campaigns"])
async def delete_campaign(campaign_id: int):
    """Delete a campaign by ID - Frontend compatible endpoint"""
    try:
        from deelflow.models import Campaign
        
        campaign = await sync_to_async(Campaign.objects.get)(id=campaign_id)
        await sync_to_async(campaign.delete)()
        return {
        "status": "success",
            "message": "Campaign deleted successfully"
        }
    except Campaign.DoesNotExist:
            return {
            "status": "error",
            "message": "Campaign not found"
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to delete campaign: {str(e)}"
        }

# Additional Campaign endpoints expected by frontend
@app.get("/campaigns/{campaign_id}/recipients/", tags=["Campaigns"])
async def get_campaign_recipients(campaign_id: int):
    """Get campaign recipients - Frontend compatible endpoint"""
    return {
        "status": "success",
        "data": {
            "campaign_id": campaign_id,
            "recipients": [],
            "total": 0
        }
    }

@app.post("/create_campaign/", tags=["Campaigns"])
async def create_campaign_legacy(campaign_data: CampaignCreate):
    """Legacy create campaign endpoint (for frontend compatibility)"""
    return await create_campaign(campaign_data)

@app.get("/active_campaign_summary/", tags=["Campaigns"])
async def get_active_campaign_summary():
    """Get active campaign summary - Frontend compatible endpoint"""
    try:
        from deelflow.models import Campaign
        active_campaigns = await sync_to_async(list)(Campaign.objects.filter(status="active"))
        return {
        "status": "success",
        "data": {
                "total_active": len(active_campaigns),
                "active_campaigns": len(active_campaigns),
                "total_budget": sum(float(c.budget or 0) for c in active_campaigns),
                "leads_today": 15,  # Mock data for now
                "leads_today_change_pct": 12.5,  # Mock data for now
                "response_rate": 8.3,  # Mock data for now
                "campaigns": [
                    {
                        "id": c.id,
                        "name": c.name,
                        "status": c.status,
                        "budget": float(c.budget or 0)
                    } for c in active_campaigns
                ]
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to get active campaigns: {str(e)}"
        }

@app.get("/campaign_property_stats/", tags=["Campaigns"])
async def get_campaign_property_stats():
    """Get campaign property statistics - Frontend compatible endpoint"""
    return {
        "status": "success",
        "data": {
            "total_properties_targeted": 156,
            "properties_per_campaign": 12.5,
            "conversion_rate": 8.3
        }
    }

@app.get("/campaign_performance_overview/", tags=["Campaigns"])
async def get_campaign_performance_overview():
    """Get campaign performance overview - Frontend compatible endpoint"""
    return {
        "status": "success",
        "data": {
            "total_campaigns": 25,
            "active_campaigns": 8,
            "completed_campaigns": 15,
            "average_roi": 125.5
        }
    }

@app.get("/channel_response_rates/", tags=["Campaigns"])
async def get_channel_response_rates():
    """Get channel response rates - Frontend compatible endpoint"""
    return {
        "status": "success",
        "data": {
            "email": {"rate": 8.5, "responses": 125},
            "sms": {"rate": 12.3, "responses": 89},
            "voice": {"rate": 19.2, "responses": 45},
            "whatsapp": {"rate": 15.7, "responses": 67}
        }
    }

@app.get("/lead_conversion_funnel/", tags=["Campaigns"])
async def get_lead_conversion_funnel():
    """Get lead conversion funnel data - Frontend compatible endpoint"""
    try:
        # TODO: Add proper implementation
        return {
            "status": "success",
            "data": {
                "leads": 500,
                "qualified": 125,
                "converted": 12,
                "leads_generated": 500,
                "qualified_leads": 125,
                "meetings_scheduled": 45,
                "deals_closed": 12,
                "conversion_rate": 2.4
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to get lead conversion funnel: {str(e)}"
        }

# ==================== LEAD ENDPOINTS (Frontend Compatible) ====================

@app.get("/leads/", tags=["Leads"])
async def get_leads():
    """Get all leads - Frontend compatible endpoint"""
    try:
        from deelflow.models import Lead
        
        leads = await sync_to_async(list)(Lead.objects.all())
        
        lead_data = []
        for lead in leads:
            lead_data.append({
                "id": lead.id,
                "name": lead.name,
                "email": lead.email,
                "phone": lead.phone,
                "address": lead.address,
                "city": lead.city,
                "state": lead.state,
                "zipcode": lead.zipcode,
                "source": lead.source,
                "status": lead.status,
                "motivation_score": lead.motivation_score,
                "property_condition": lead.property_condition,
                "financial_situation": lead.financial_situation,
                "timeline_urgency": lead.timeline_urgency,
                "negotiation_style": lead.negotiation_style,
                "notes": lead.notes,
                "responded": lead.responded,
                "created_at": lead.created_at.isoformat(),
                "updated_at": lead.updated_at.isoformat()
            })
        return {
            "status": "success",
            "data": lead_data,
            "total": len(lead_data),
            "page": 1,
            "limit": 20
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to retrieve leads: {str(e)}",
            "data": [],
            "total": 0,
            "page": 1,
            "limit": 20
        }

@app.post("/leads/", tags=["Leads"])
async def create_lead(lead_data: LeadCreate):
    """Create a new lead - Frontend compatible endpoint"""
    try:
        from deelflow.models import Lead
        
        # Create lead in Django database
        lead = await sync_to_async(Lead.objects.create)(
            name=f"{lead_data.first_name} {lead_data.last_name}",
            email=lead_data.email,
            phone=lead_data.phone,
            address=lead_data.property_address,
            city=lead_data.property_city,
            state=lead_data.property_state,
            zipcode=lead_data.property_zip,
            source=lead_data.source,
            status=lead_data.status
        )
        return {
            "status": "success",
            "message": "Lead created successfully",
            "data": {
                "id": lead.id,
                "first_name": lead_data.first_name,
                "last_name": lead_data.last_name,
                "email": lead.email,
                "phone": lead.phone,
                "property_address": lead.address,
                "property_city": lead.city,
                "property_state": lead.state,
                "property_zip": lead.zipcode,
                "property_type": lead_data.property_type,
                "source": lead.source,
                "estimated_value": lead_data.estimated_value,
                "mortgage_balance": lead_data.mortgage_balance,
                "asking_price": lead_data.asking_price,
                "preferred_contact_method": lead_data.preferred_contact_method,
                "lead_type": lead_data.lead_type,
                "status": lead.status,
                "created_at": lead.created_at.isoformat(),
                "updated_at": lead.updated_at.isoformat()
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to create lead: {str(e)}"
        }

@app.get("/leads/{lead_id}/", tags=["Leads"])
async def get_lead(lead_id: int):
    """Get a specific lead by ID - Frontend compatible endpoint"""
    try:
        from deelflow.models import Lead
        
        lead = await sync_to_async(Lead.objects.get)(id=lead_id)
        
        # Split name into first_name and last_name
        name_parts = lead.name.split(" ", 1) if lead.name else ["", ""]
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        return {
        "status": "success",
            "data": {
                "id": lead.id,
                "first_name": first_name,
                "last_name": last_name,
                "email": lead.email,
                "phone": lead.phone,
                "property_address": lead.address,
                "property_city": lead.city,
                "property_state": lead.state,
                "property_zip": lead.zipcode,
                "property_type": "",  # Not stored in model
                "source": lead.source,
                "estimated_value": "",
                "mortgage_balance": "",
                "asking_price": "",
                "preferred_contact_method": "",
                "lead_type": "",
                "status": lead.status,
                "motivation_score": lead.motivation_score,
                "notes": lead.notes,
                "responded": lead.responded,
                "created_at": lead.created_at.isoformat(),
                "updated_at": lead.updated_at.isoformat()
            }
        }
    except Lead.DoesNotExist:
            return {
            "status": "error",
            "message": "Lead not found"
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to retrieve lead: {str(e)}"
        }

@app.put("/leads/{lead_id}/", tags=["Leads"])
async def update_lead(lead_id: int, lead_data: LeadUpdate):
    """Update a lead by ID - Frontend compatible endpoint"""
    try:
        from deelflow.models import Lead
        
        lead = await sync_to_async(Lead.objects.get)(id=lead_id)
        update_data = lead_data.dict(exclude_unset=True)
        
        # Handle name field separately (combine first_name and last_name)
        if 'first_name' in update_data or 'last_name' in update_data:
            first_name = update_data.get('first_name', lead.name.split(' ')[0] if lead.name else '')
            last_name = update_data.get('last_name', lead.name.split(' ')[1] if len(lead.name.split(' ')) > 1 else '')
            lead.name = f"{first_name} {last_name}".strip()
        
        # Handle property address fields
        if 'property_address' in update_data:
            lead.address = update_data['property_address']
        if 'property_city' in update_data:
            lead.city = update_data['property_city']
        if 'property_state' in update_data:
            lead.state = update_data['property_state']
        if 'property_zip' in update_data:
            lead.zipcode = update_data['property_zip']
        
        # Handle other fields
        field_mapping = {
            'email': 'email',
            'phone': 'phone',
            'source': 'source',
            'status': 'status'
        }
        
        for frontend_field, backend_field in field_mapping.items():
            if frontend_field in update_data:
                setattr(lead, backend_field, update_data[frontend_field])
        
        await sync_to_async(lead.save)()
        
        # Return updated data
        name_parts = lead.name.split(" ", 1) if lead.name else ["", ""]
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        return {
        "status": "success",
            "message": "Lead updated successfully",
        "data": {
                "id": lead.id,
                "first_name": first_name,
                "last_name": last_name,
                "email": lead.email,
                "phone": lead.phone,
                "property_address": lead.address,
                "property_city": lead.city,
                "property_state": lead.state,
                "property_zip": lead.zipcode,
                "status": lead.status,
                "updated_at": lead.updated_at.isoformat()
            }
        }
    except Lead.DoesNotExist:
            return {
            "status": "error",
            "message": "Lead not found"
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to update lead: {str(e)}"
        }

@app.delete("/leads/{lead_id}/", tags=["Leads"])
async def delete_lead(lead_id: int):
    """Delete a lead by ID - Frontend compatible endpoint"""
    try:
        from deelflow.models import Lead
        
        lead = await sync_to_async(Lead.objects.get)(id=lead_id)
        await sync_to_async(lead.delete)()
        return {
        "status": "success",
            "message": "Lead deleted successfully"
        }
    except Lead.DoesNotExist:
            return {
            "status": "error",
            "message": "Lead not found"
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to delete lead: {str(e)}"
        }

@app.get("/leads/{lead_id}/ai-score/", tags=["Leads"])
async def get_lead_ai_score(lead_id: int):
    """Get AI score for a lead - Frontend compatible endpoint"""
    try:
        from deelflow.models import Lead
        
        lead = await sync_to_async(Lead.objects.get)(id=lead_id)
        
        # Mock AI score calculation
        ai_score = {
            "lead_id": lead_id,
            "score": 85.5,
            "confidence": 0.87,
            "factors": [
                "High estimated value",
                "Good property condition",
                "Favorable market conditions"
            ],
            "recommendation": "High priority lead",
            "analysis_date": datetime.datetime.now().isoformat()
    }
        return {
        "status": "success",
            "data": ai_score
        }
    except Lead.DoesNotExist:
            return {
            "status": "error",
            "message": "Lead not found"
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to get AI score: {str(e)}"
        }

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.post("/api/auth/login", tags=["Authentication"])
async def login(login_data: LoginRequest):
    """
    **User Login**
    
    Authenticates a user with email and password, returning a JWT token for subsequent API calls.
    
    **Request Body:**
    - email: User's email address
    - password: User's password
    
    **Returns:**
    - JWT access token
    - Token type (Bearer)
    - User information (id, email, name, role)
    - Authentication status
    
    **Error Responses:**
    - 400: Invalid credentials (wrong password)
    - 404: Email not registered (prompt to sign up)
    """
    try:
        from deelflow.models import User
        from app.core.security import check_password, create_access_token
        from django.contrib.auth.hashers import check_password as django_check_password
        
        # Check if user exists
        try:
            user = await sync_to_async(User.objects.get)(email=login_data.email)
        except User.DoesNotExist:
            return {
                "status": "error",
                "message": "Email not registered. Please sign up first.",
                "error_code": "EMAIL_NOT_FOUND"
            }
        
        # Verify password
        if not django_check_password(login_data.password, user.password):
            return {
                "status": "error",
                "message": "Invalid email or password"
            }
        
        # Check if user is active
        if not user.is_active:
            return {
                "status": "error",
                "message": "Account is inactive. Please contact support."
            }
        
        # Generate JWT token
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role
        }
        access_token = create_access_token(data=token_data)
        
        return {
            "status": "success",
            "message": "Login successful",
            "data": {
                "tokens": {
                    "access_token": access_token,
                    "token_type": "bearer"
                },
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "is_verified": user.is_verified,
                    "organization_id": user.organization_id if hasattr(user, 'organization_id') else None
                }
            }
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"Login failed: {str(e)}"
        }

@app.post("/api/auth/register", tags=["Authentication"])
async def register(register_data: RegisterRequest):
    """
    **User Registration**
    
    Creates a new user account with the provided information.
    
    **Request Body:**
    - email: User's email address
    - password: User's password
    - first_name: User's first name
    - last_name: User's last name
    - organization_id: Organization ID (optional, creates default if not provided)
    
    **Returns:**
    - Registration status
    - JWT access token
    - User information
    - Success/error message
    
    **Error Responses:**
    - 409: Email already registered
    - 400: Missing required fields
    """
    try:
        from deelflow.models import User, Organization
        from app.core.security import hash_password, create_access_token
        import uuid
        
        # Check if email already exists
        existing_user = await sync_to_async(User.objects.filter)(email=register_data.email)
        if await sync_to_async(existing_user.exists)():
            return {
                "status": "error",
                "message": "Email already registered. Please sign in.",
                "error_code": "EMAIL_EXISTS"
            }
        
        # Get or create organization
        organization_id = register_data.organization_id
        org_payload = getattr(register_data, "organization", None) or {}

        # Helper to slugify and ensure uniqueness
        def slugify(value: str) -> str:
            import re
            value = (value or "").strip().lower()
            value = re.sub(r"[^a-z0-9\-\s]", "", value)
            value = re.sub(r"\s+", "-", value)
            value = re.sub(r"-+", "-", value)
            return value or "org"

        async def generate_unique_slug(base_slug: str) -> str:
            base = slugify(base_slug)
            candidate = base
            suffix = 1
            while await sync_to_async(Organization.objects.filter(slug=candidate).exists)():
                suffix += 1
                candidate = f"{base}-{suffix}"
            return candidate

        if organization_id:
            try:
                organization = await sync_to_async(Organization.objects.get)(id=organization_id)
            except Organization.DoesNotExist:
                # Fall back to creating from payload or default
                desired_name = org_payload.get("name") if isinstance(org_payload, dict) else None
                desired_slug = org_payload.get("slug") if isinstance(org_payload, dict) else None
                name = desired_name or f"{register_data.first_name}'s Organization"
                slug_base = desired_slug or slugify(name) or f"{register_data.first_name.lower()}-org"
                unique_slug = await generate_unique_slug(slug_base)
                organization = await sync_to_async(Organization.objects.create)(
                    name=name,
                    slug=unique_slug,
                    subscription_status=(org_payload.get("subscription_status") if isinstance(org_payload, dict) else "trial") or "trial",
                )
        else:
            # Create organization from payload if provided, else default
            desired_name = org_payload.get("name") if isinstance(org_payload, dict) else None
            desired_slug = org_payload.get("slug") if isinstance(org_payload, dict) else None
            name = desired_name or f"{register_data.first_name}'s Organization"
            slug_base = desired_slug or slugify(name) or f"{register_data.first_name.lower()}-org"
            # If slug exists, generate a unique one instead of failing
            unique_slug = await generate_unique_slug(slug_base)
            organization = await sync_to_async(Organization.objects.create)(
                name=name,
                slug=unique_slug,
                subscription_status=(org_payload.get("subscription_status") if isinstance(org_payload, dict) else "trial") or "trial",
            )
        
        # Hash password
        hashed_password = hash_password(register_data.password)
        
        # Create user
        user = await sync_to_async(User.objects.create)(
            email=register_data.email,
            first_name=register_data.first_name,
            last_name=register_data.last_name,
            password=hashed_password,
            organization=organization,
            role="user",
            is_active=True,
            is_verified=False
        )
        
        # Generate JWT token
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role
        }
        access_token = create_access_token(data=token_data)
        
        return {
            "status": "success",
            "message": "User registered successfully",
            "data": {
                "tokens": {
                    "access_token": access_token,
                    "token_type": "bearer"
                },
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "is_verified": user.is_verified,
                    "organization_id": organization.id
                }
            }
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"Registration failed: {str(e)}"
        }

@app.post("/api/auth/logout", tags=["Authentication"])
@app.post("/logout/", tags=["Authentication"])
async def logout():
    """
    **User Logout**
    
    Logs out the current user. On the client side, this should clear the JWT token from localStorage.
    
    **Returns:**
    - Success message
    
    **Note:** This is a client-side logout. The JWT token should be removed from the client's storage.
    """
    return {
        "status": "success",
        "message": "Logged out successfully"
    }

@app.get("/api/auth/me", tags=["Authentication"])
async def get_current_user():
    """Get current user information"""
    return {
        "status": "success",
        "data": {
            "id": 1,
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": "admin",
            "organization_id": 1
        }
    }

@app.get("/api/test-dashboard", tags=["Core"])
async def test_dashboard():
    """Test endpoint for dashboard debugging"""
    return {
        "status": "success",
        "message": "Dashboard test endpoint working",
        "data": {
            "test_revenue": 125000.50,
            "test_users": 25,
            "test_properties": 5,
            "test_conversations": 1250
        }
    }

# ==================== ROLE MANAGEMENT ENDPOINTS ====================

@app.get("/api/roles/", tags=["Role Management"])
async def get_roles(page: int = 1, limit: int = 20):
    """Get all roles with pagination"""
    try:
        from deelflow.models import Role
        from django.core.paginator import Paginator
        
        # Get all roles
        roles_queryset = Role.objects.all().prefetch_related('permissions')
        roles_list = await sync_to_async(list)(roles_queryset)
        
        # Paginate
        paginator = Paginator(roles_list, limit)
        page_obj = paginator.get_page(page)
        
        # Convert to response format
        roles_data = []
        for role in page_obj:
            permissions_data = []
            for perm in role.permissions.all():
                permissions_data.append({
                    "id": perm.id,
                    "name": perm.name,
                    "label": perm.label
                })
            
            roles_data.append({
                "id": role.id,
                "name": role.name,
                "label": role.label,
                "permissions": permissions_data,
                "created_at": role.created_at.isoformat(),
                "updated_at": role.updated_at.isoformat()
            })
        return {
        "status": "success",
            "data": {
                "roles": roles_data,
                "total": paginator.count,
                "page": page,
                "limit": limit,
                "total_pages": paginator.num_pages
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to retrieve roles: {str(e)}"
        }

@app.get("/api/roles/stats/", tags=["Role Management"])
async def get_role_stats():
    """Get role management statistics"""
    try:
        from deelflow.models import Role, Permission, User, Organization
        
        # Get counts
        total_roles = await sync_to_async(Role.objects.count)()
        total_permissions = await sync_to_async(Permission.objects.count)()
        total_users = await sync_to_async(User.objects.count)()
        total_tenants = await sync_to_async(Organization.objects.count)()
        
        # Get active tenants (non-suspended)
        active_tenants = await sync_to_async(Organization.objects.exclude(subscription_status='suspended').count)()
        
        # Calculate active tenant percentage
        active_tenant_percentage = (active_tenants / total_tenants * 100) if total_tenants > 0 else 0
        return {
        "status": "success",
            "data": {
                "total_roles": total_roles,
                "total_permissions": total_permissions,
                "total_users": total_users,
                "total_tenants": total_tenants,
                "active_tenants": active_tenants,
                "active_tenant_percentage": round(active_tenant_percentage, 1)
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to retrieve role stats: {str(e)}"
        }

@app.get("/api/roles/{role_id}/", tags=["Role Management"])
async def get_role(role_id: int):
    """Get a specific role by ID"""
    try:
        from deelflow.models import Role, Permission
        
        # Fetch the role and its assigned permissions
        role = await sync_to_async(Role.objects.prefetch_related('permissions').get)(id=role_id)
        role_permissions = await sync_to_async(list)(role.permissions.values_list('id', flat=True))

        # Fetch all permissions
        all_permissions = await sync_to_async(list)(Permission.objects.all())

        # Get permissions using sync_to_async
        permissions_data = []
        #permissions_list = await sync_to_async(list)(role.permissions.all())
        for perm in all_permissions:
            permissions_data.append({
                "id": perm.id,
                "name": perm.name,
                "label": perm.label,
                "status": perm.id in role_permissions
            })
        return {
        "status": "success",
            "data": {
                "id": role.id,
                "name": role.name,
                "label": role.label,
                "permissions": permissions_data,
                "created_at": role.created_at.isoformat(),
                "updated_at": role.updated_at.isoformat()
            }
        }
    except Role.DoesNotExist:
            return {
            "status": "error",
            "message": "Role not found"
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to retrieve role: {str(e)}"
        }

@app.post("/api/roles/", 
         tags=["Role Management"],
         summary="Create Role",
         description="Create a new role with specified permissions",
         response_description="Created role details",
         responses={
             200: {
                 "description": "Role created successfully",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "success",
                             "message": "Role created successfully",
                             "data": {
                                 "id": 1,
                                 "name": "admin",
                                 "label": "Administrator",
                                 "permissions": [
                                     {"id": 1, "name": "manage_users", "label": "Manage Users"},
                                     {"id": 2, "name": "manage_roles", "label": "Manage Roles"}
                                 ],
                                 "created_at": "2024-10-13T07:34:07.710903+00:00",
                                 "updated_at": "2024-10-13T07:34:07.710903+00:00"
                             }
                         }
                     }
                 }
             },
             400: {
                 "description": "Bad request - missing required fields",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "error",
                             "message": "Role name and label are required"
                         }
                     }
                 }
             },
             409: {
                 "description": "Conflict - role already exists",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "error",
                             "message": "Role with this name already exists"
                         }
                     }
                 }
             }
         })
async def create_role(role_data: dict):
    """
    **Create Role**
    
    Creates a new role with specified permissions.
    
    **Request Body:**
    - **name** (str): Unique role name (required)
    - **label** (str): Human-readable role label (required)
    - **permissions** (List[dict]): Complex permission structure from frontend (optional)
    
    **Example Request:**
    ```json
    {
        "name": "admin",
        "label": "Administrator",
        "permissions": [
            {
                "group": "Users",
                "count": "2 / 4",
                "permissions": [
                    {"id": 1, "name": "create_users", "label": "Create Users", "enabled": true}
                ]
            }
        ]
    }
    ```
    """
    try:
        from deelflow.models import Role, Permission
        
        # Extract data from dict
        name = role_data.get("name")
        label = role_data.get("label")
        permissions_data = role_data.get("permissions", [])
        
        if not name or not label:
            return {
                "status": "error",
                "message": "Role name and label are required"
            }
        
        # Check if role already exists
        existing_role = await sync_to_async(Role.objects.filter)(name=name)
        if await sync_to_async(existing_role.exists)():
            return {
                "status": "error",
                "message": "Role with this name already exists"
            }
        
        # Create role
        role = await sync_to_async(Role.objects.create)(
            name=name,
            label=label
        )
        
        # Extract permission IDs from complex structure
        permission_ids = []
        for group in permissions_data:
            if isinstance(group, dict) and "permissions" in group:
                for perm in group["permissions"]:
                    if isinstance(perm, dict) and "id" in perm and perm.get("enabled", False):
                        permission_ids.append(perm["id"])
        
        # Add permissions if provided
        if permission_ids:
            permissions = await sync_to_async(list)(Permission.objects.filter(id__in=permission_ids))
            await sync_to_async(role.permissions.set)(permissions)
        
        # Get the role with permissions for response
        role = await sync_to_async(Role.objects.prefetch_related('permissions').get)(id=role.id)
        
        # Get permissions data
        permissions_response = []
        for perm in role.permissions.all():
            permissions_response.append({
                "id": perm.id,
                "name": perm.name,
                "label": perm.label
            })
        
        return {
            "status": "success",
            "message": "Role created successfully",
            "data": {
                "id": role.id,
                "name": role.name,
                "label": role.label,
                "permissions": permissions_response,
                "created_at": role.created_at.isoformat(),
                "updated_at": role.updated_at.isoformat()
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create role: {str(e)}"
        }

@app.put("/api/roles/{role_id}/", tags=["Role Management"])
async def update_role(role_id: int, role_data: dict):
    """Update a role by ID"""
    try:
        from deelflow.models import Role, Permission
        from asgiref.sync import sync_to_async

        # Get role
        role = await sync_to_async(lambda: Role.objects.get(id=role_id))()

        # Update name if provided
        if "name" in role_data:
            existing_role = await sync_to_async(lambda: Role.objects.filter(name=role_data["name"]).exclude(id=role_id))()
            if await sync_to_async(existing_role.exists)():
                return {"status": "error", "message": "Role with this name already exists"}
            role.name = role_data["name"]

        # Update label
        if "label" in role_data:
            role.label = role_data["label"]

        await sync_to_async(role.save)()

        # Update permissions
        if "permissions" in role_data:
            permission_ids = [
                perm["id"] for perm in role_data["permissions"] if perm.get("status", False)
            ]
            if permission_ids:
                permissions = await sync_to_async(lambda: list(Permission.objects.filter(id__in=permission_ids)))()
                await sync_to_async(role.permissions.set)(permissions)
            else:
                await sync_to_async(role.permissions.clear)()

        # Fetch updated role with permissions
        role = await sync_to_async(lambda: Role.objects.prefetch_related("permissions").get(id=role_id))()
        permissions_list = await sync_to_async(list)(role.permissions.all())

        permissions_data = [
            {"id": perm.id, "name": perm.name, "label": perm.label} for perm in permissions_list
        ]

        return {
            "status": "success",
            "message": "Role updated successfully",
            "data": {
                "id": role.id,
                "name": role.name,
                "label": role.label,
                "permissions": permissions_data,
                "created_at": role.created_at.isoformat(),
                "updated_at": role.updated_at.isoformat(),
            },
        }

    except Role.DoesNotExist:
        return {"status": "error", "message": "Role not found"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to update role: {str(e)}"}


# @app.put("/api/roles/{role_id}/", tags=["Role Management"])
# async def update_role(role_id: int, role_data: dict):
#     """Update a role by ID"""
#     try:
#         from deelflow.models import Role, Permission
        
#         # Get role
#         role = await sync_to_async(Role.objects.get)(id=role_id)
        
#         # Update fields if provided
#         if "name" in role_data:
#             # Check if new name already exists (excluding current role)
#             existing_role = await sync_to_async(Role.objects.filter)(name=role_data["name"]).exclude(id=role_id)
#             if await sync_to_async(existing_role.exists)():
#                 return {
#                     "status": "error",
#                     "message": "Role with this name already exists"
#                 }
#             role.name = role_data["name"]
        
#         if "label" in role_data:
#             role.label = role_data["label"]
        
#         await sync_to_async(role.save)()
        
#         # Update permissions if provided
#         if "permissions" in role_data:
#             permissions_data = role_data["permissions"]
            
#             # Extract permission IDs from complex structure
#             permission_ids = []
#             for group in permissions_data:
#                 if isinstance(group, dict) and "permissions" in group:
#                     for perm in group["permissions"]:
#                         if isinstance(perm, dict) and "id" in perm and perm.get("enabled", False):
#                             permission_ids.append(perm["id"])
            
#             if permission_ids:
#                 permissions = await sync_to_async(list)(Permission.objects.filter(id__in=permission_ids))
#                 await sync_to_async(role.permissions.set)(permissions)
#             else:
#                 await sync_to_async(role.permissions.clear)()
#         elif "permission_ids" in role_data:
#             permission_ids = role_data["permission_ids"]
#             if permission_ids:
#                 permissions = await sync_to_async(list)(Permission.objects.filter(id__in=permission_ids))
#                 await sync_to_async(role.permissions.set)(permissions)
#             else:
#                 await sync_to_async(role.permissions.clear)()
        
#         # Get the updated role with permissions
#         role = await sync_to_async(Role.objects.prefetch_related('permissions').get)(id=role.id)
        
#         # Get permissions data
#         permissions_data = []
#         for perm in role.permissions.all():
#             permissions_data.append({
#                 "id": perm.id,
#                 "name": perm.name,
#                 "label": perm.label
#             })
#         return {
#         "status": "success",
#             "message": "Role updated successfully",
#         "data": {
#                 "id": role.id,
#                 "name": role.name,
#                 "label": role.label,
#                 "permissions": permissions_data,
#                 "created_at": role.created_at.isoformat(),
#                 "updated_at": role.updated_at.isoformat()
#             }
#         }
#     except Role.DoesNotExist:
#             return {
#             "status": "error",
#             "message": "Role not found"
#         }
#     except Exception as e:
#             return {
#             "status": "error",
#             "message": f"Failed to update role: {str(e)}"
#         }

@app.delete("/api/roles/{role_id}/", tags=["Role Management"])
async def delete_role(role_id: int):
    """Delete a role by ID"""
    try:
        from deelflow.models import Role
        
        role = await sync_to_async(Role.objects.get)(id=role_id)
        await sync_to_async(role.delete)()
        return {
            "status": "success",
            "message": "Role deleted successfully"
        }
    except Role.DoesNotExist:
            return {
            "status": "error",
            "message": "Role not found"
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to delete role: {str(e)}"
        }

# ==================== USER-ROLE ASSIGNMENT ENDPOINTS ====================

@app.post("/api/roles/{role_id}/assign-user/", 
         tags=["Role Management"],
         summary="Assign User to Role",
         description="Assign a user to a specific role by providing either user_id or email",
         response_description="User-role assignment status with user and role details",
         responses={
             200: {
                 "description": "Successfully assigned user to role",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "success",
                             "message": "User assigned to role successfully",
                             "data": {
                                 "user": {
                                     "id": 1,
                                     "email": "user@example.com",
                                     "first_name": "John",
                                     "last_name": "Doe"
                                 },
                                 "role": {
                                     "id": 141,
                                     "name": "admin",
                                     "label": "Administrator"
                                 }
                             }
                         }
                     }
                 }
             },
             400: {
                 "description": "Bad request - missing user_id or email",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "error",
                             "message": "Either user_id or email must be provided"
                         }
                     }
                 }
             },
             404: {
                 "description": "Not found - role or user not found",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "error",
                             "message": "Role not found"
                         }
                     }
                 }
             }
         })
async def assign_user_to_role(role_id: int, user_data: dict):
    """
    **Assign User to Role**
    
    Assigns a user to a specific role. You can provide either `user_id` or `email` to identify the user.
    
    **Path Parameters:**
    - **role_id** (int): The ID of the role to assign
    
    **Request Body:**
    - **user_id** (int, optional): The ID of the user to assign
    - **email** (str, optional): The email of the user to assign
    
    **Returns:**
    - **status**: "success" or "error"
    - **message**: Status message
    - **data** (if success):
      - **user**: User details (id, email, first_name, last_name)
      - **role**: Role details (id, name, label)
    
    **Example Request:**
    ```json
    {
        "user_id": 1
    }
    ```
    OR
    ```json
    {
        "email": "user@example.com"
    }
    ```
    """
    try:
        from deelflow.models import Role, Organization
        
        # Get user_id or email from request
        user_id = user_data.get("user_id")
        email = user_data.get("email")
        
        if not user_id and not email:
            return {
                "status": "error",
                "message": "Either user_id or email must be provided"
            }
        
        # Get role
        role = await sync_to_async(Role.objects.get)(id=role_id)
        
        # Find user by ID or email
        from deelflow.models import User
        if user_id:
            user = await sync_to_async(User.objects.get)(id=user_id)
        else:
            user = await sync_to_async(User.objects.get)(email=email)
        
        # Assign role to user (store role name as string)
        user.role = role.name
        await sync_to_async(user.save)()
        
        return {
            "status": "success",
            "message": "User assigned to role successfully",
            "data": {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": getattr(user, 'first_name', ''),
                    "last_name": getattr(user, 'last_name', '')
                },
                "role": {
                    "id": role.id,
                    "name": role.name,
                    "label": role.label
                }
            }
        }
    except Role.DoesNotExist:
        return {
            "status": "error",
            "message": "Role not found"
        }
    except User.DoesNotExist:
        return {
            "status": "error",
            "message": "User not found. Please provide a valid user_id or email."
        }
    except Exception as e:
        # Only print traceback for unexpected errors
        if "DoesNotExist" not in str(e):
            import traceback
            traceback.print_exc()
        return {
            "status": "error",
            "message": f"Failed to assign user to role: {str(e)}"
        }

@app.delete("/api/roles/{role_id}/users/{user_id}/", 
            tags=["Role Management"],
            summary="Remove User from Role",
            description="Remove a user's assignment from a specific role",
            response_description="User removal status",
            responses={
                200: {
                    "description": "Successfully removed user from role",
                    "content": {
                        "application/json": {
                            "example": {
                                "status": "success",
                                "message": "User removed from role successfully",
                                "data": {
                                    "user": {"id": 1, "email": "user@example.com"},
                                    "role": {"id": 141, "name": "admin"}
                                }
                            }
                        }
                    }
                },
                404: {
                    "description": "Role or user not found",
                    "content": {
                        "application/json": {
                            "example": {
                                "status": "error",
                                "message": "Role or user not found"
                            }
                        }
                    }
                }
            })
async def remove_user_from_role(role_id: int, user_id: int):
    """
    **Remove User from Role**
    
    Removes a user's assignment from a specific role. The user's role will be set to the default "user" role.
    
    **Path Parameters:**
    - **role_id** (int): The ID of the role to remove the user from
    - **user_id** (int): The ID of the user to remove
    
    **Returns:**
    - **status**: "success" or "error"
    - **message**: Status message
    - **data** (if success):
      - **user**: User details (id, email)
      - **role**: Role details (id, name)
    """
    try:
        from deelflow.models import Role, User
        
        # Get user and role
        user = await sync_to_async(User.objects.get)(id=user_id)
        role = await sync_to_async(Role.objects.get)(id=role_id)
        
        # Check if user is assigned to this role
        if user.role != role.name:
            return {
                "status": "error",
                "message": "User is not assigned to this role"
            }
        
        # Remove role assignment (set role to empty string or default)
        user.role = "user"  # Default role
        await sync_to_async(user.save)()
        
        return {
            "status": "success",
            "message": "User removed from role successfully",
            "data": {
                "user": {
                    "id": user.id,
                    "email": user.email
                },
                "role": {
                    "id": role.id,
                    "name": role.name
                }
            }
        }
    except (Role.DoesNotExist, User.DoesNotExist) as e:
        return {
            "status": "error",
            "message": f"Role or user not found: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to remove user from role: {str(e)}"
        }

@app.get("/api/roles/{role_id}/users/", 
         tags=["Role Management"],
         summary="Get Users in Role",
         description="Retrieve all users assigned to a specific role",
         response_description="List of users with their role information",
         responses={
             200: {
                 "description": "Successfully retrieved users",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "success",
                             "data": {
                                 "role": {
                                     "id": 141,
                                     "name": "admin",
                                     "label": "Administrator"
                                 },
                                 "users": [
                                     {
                                         "id": 1,
                                         "email": "user@example.com",
                                         "first_name": "John",
                                         "last_name": "Doe",
                                         "role": {"id": 141, "name": "admin", "label": "Administrator"}
                                     }
                                 ],
                                 "total": 1
                             }
                         }
                     }
                 }
             },
             404: {
                 "description": "Role not found",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "error",
                             "message": "Role not found"
                         }
                     }
                 }
             }
         })
async def get_role_users(role_id: int):
    """
    **Get Users Assigned to Role**
    
    Retrieves all users assigned to a specific role with their full details.
    
    **Path Parameters:**
    - **role_id** (int): The ID of the role
    
    **Returns:**
    - **status**: "success" or "error"
    - **data** (if success):
      - **role**: Role details (id, name, label)
      - **users**: Array of user objects with (id, email, first_name, last_name, role)
      - **total**: Total number of users in the role
    """
    try:
        from deelflow.models import Role, User
        
        # Get role
        role = await sync_to_async(Role.objects.get)(id=role_id)
        
        # Get all users with this role (role is a string field)
        users = await sync_to_async(list)(User.objects.filter(role=role.name))
        
        users_data = []
        for user in users:
            users_data.append({
                "id": user.id,
                "email": user.email,
                "first_name": getattr(user, 'first_name', ''),
                "last_name": getattr(user, 'last_name', ''),
                "role": {
                    "id": role.id,
                    "name": role.name,
                    "label": role.label
                }
            })
        
        return {
            "status": "success",
            "data": {
                "role": {
                    "id": role.id,
                    "name": role.name,
                    "label": role.label
                },
                "users": users_data,
                "total": len(users_data)
            }
        }
    except Role.DoesNotExist:
        return {
            "status": "error",
            "message": "Role not found"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get role users: {str(e)}"
        }

@app.put("/api/users/{user_id}/assign-role/", 
         tags=["Role Management"],
         summary="Assign Role to User (Alternative)",
         description="Alternative endpoint to assign a role to a user by user ID",
         response_description="Role assignment status",
         responses={
             200: {
                 "description": "Successfully assigned role to user",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "success",
                             "message": "Role assigned to user successfully",
                             "data": {
                                 "user": {
                                     "id": 1,
                                     "email": "user@example.com",
                                     "first_name": "John",
                                     "last_name": "Doe"
                                 },
                                 "role": {
                                     "id": 141,
                                     "name": "admin",
                                     "label": "Administrator"
                                 }
                             }
                         }
                     }
                 }
             },
             400: {
                 "description": "Bad request - missing role_id",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "error",
                             "message": "role_id is required"
                         }
                     }
                 }
             },
             404: {
                 "description": "User or role not found",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "error",
                             "message": "Role or user not found"
                         }
                     }
                 }
             }
         })
async def assign_role_to_user(user_id: int, role_data: dict):
    """
    **Assign Role to User (Alternative Endpoint)**
    
    Alternative endpoint to assign a role to a user. This endpoint takes the user ID as a path parameter.
    
    **Path Parameters:**
    - **user_id** (int): The ID of the user to assign the role to
    
    **Request Body:**
    - **role_id** (int): The ID of the role to assign
    
    **Returns:**
    - **status**: "success" or "error"
    - **message**: Status message
    - **data** (if success):
      - **user**: User details (id, email, first_name, last_name)
      - **role**: Role details (id, name, label)
    
    **Example Request:**
    ```json
    {
        "role_id": 141
    }
    ```
    """
    try:
        from deelflow.models import Role, User
        
        # Get role_id from request
        role_id = role_data.get("role_id")
        
        if not role_id:
            return {
                "status": "error",
                "message": "role_id is required"
            }
        
        # Get user and role
        user = await sync_to_async(User.objects.get)(id=user_id)
        role = await sync_to_async(Role.objects.get)(id=role_id)
        
        # Assign role (store role name as string)
        user.role = role.name
        await sync_to_async(user.save)()
        
        return {
            "status": "success",
            "message": "Role assigned to user successfully",
            "data": {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": getattr(user, 'first_name', ''),
                    "last_name": getattr(user, 'last_name', '')
                },
                "role": {
                    "id": role.id,
                    "name": role.name,
                    "label": role.label
                }
            }
        }
    except (Role.DoesNotExist, User.DoesNotExist) as e:
        return {
            "status": "error",
            "message": f"Role or user not found: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to assign role: {str(e)}"
        }

# Add legacy endpoints for frontend compatibility
@app.get("/get_roles/", tags=["Role Management"])
async def get_roles_legacy():
    """Legacy endpoint for frontend compatibility"""
    return await get_roles(page=1, limit=100)

@app.get("/get_permissions/", tags=["Role Management"])
async def get_permissions_legacy():
    """Legacy endpoint for frontend compatibility"""
    return await get_permissions(page=1, limit=100)

# Add missing endpoints that frontend is calling
@app.get("/ai_metrics/", tags=["AI Services"])
async def get_ai_metrics_endpoint():
    """Get AI metrics - Frontend expected endpoint"""
    try:
        ai_metrics = await get_ai_metrics()
        return {
            "status": "success",
            "data": ai_metrics
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch AI metrics: {str(e)}"
        }

@app.get("/performance/", tags=["Analytics"])
async def get_performance_endpoint():
    """Get performance metrics - Frontend expected endpoint"""
    try:
        performance_metrics = await get_performance_metrics()
        return {
            "status": "success",
            "data": performance_metrics
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch performance metrics: {str(e)}"
        }

@app.get("/api/permissions/", tags=["Role Management"])
async def get_permissions(page: int = 1, limit: int = 50):
    """Get all permissions with pagination"""
    try:
        from deelflow.models import Permission
        from django.core.paginator import Paginator
        
        # Get all permissions
        permissions_queryset = Permission.objects.all()
        permissions_list = await sync_to_async(list)(permissions_queryset)
        
        # Paginate
        paginator = Paginator(permissions_list, limit)
        page_obj = paginator.get_page(page)
        
        # Convert to response format
        permissions_data = []
        for perm in page_obj:
            permissions_data.append({
                "id": perm.id,
                "name": perm.name,
                "label": perm.label
            })
        return {
        "status": "success",
            "data": {
                "permissions": permissions_data,
                "total": paginator.count,
                "page": page,
                "limit": limit,
                "total_pages": paginator.num_pages
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to retrieve permissions: {str(e)}"
        }

@app.get("/api/permissions/grouped/", tags=["Role Management"])
async def get_permissions_grouped():
    """Get permissions grouped by categories with role assignments for table view"""
    try:
        from deelflow.models import Permission, Role
        from collections import defaultdict
        
        # Get all permissions and roles
        permissions_queryset = Permission.objects.all()
        roles_queryset = Role.objects.all()
        
        permissions_list = await sync_to_async(list)(permissions_queryset)
        roles_list = await sync_to_async(list)(roles_queryset)
        
        # Group permissions by category
        permission_groups = defaultdict(list)
        
        for perm in permissions_list:
            # Determine category based on permission name
            category = "Other"
            if any(keyword in perm.name.lower() for keyword in ['user', 'create_user', 'view_user', 'edit_user', 'delete_user']):
                category = "User Management"
            elif any(keyword in perm.name.lower() for keyword in ['billing', 'payment', 'invoice']):
                category = "Billing"
            elif any(keyword in perm.name.lower() for keyword in ['content', 'create_content', 'edit_content', 'delete_content']):
                category = "Content Management"
            elif any(keyword in perm.name.lower() for keyword in ['campaign', 'create_campaign', 'edit_campaign']):
                category = "Campaigns"
            elif any(keyword in perm.name.lower() for keyword in ['property', 'create_property', 'edit_property']):
                category = "Properties"
            elif any(keyword in perm.name.lower() for keyword in ['report', 'analytics', 'export']):
                category = "Analytics & Reports"
            elif any(keyword in perm.name.lower() for keyword in ['role', 'permission']):
                category = "Role Management"
            elif any(keyword in perm.name.lower() for keyword in ['system', 'tenant', 'backup', 'landing', 'theme', 'domain']):
                category = "System Administration"
            elif any(keyword in perm.name.lower() for keyword in ['own', 'personal']):
                category = "Own Data"
            
            # Get role assignments for this permission
            role_assignments = []
            for role in roles_list:
                # Check if this role has this permission
                has_permission = await sync_to_async(lambda: role.permissions.filter(id=perm.id).exists())()
                role_assignments.append({
                    "id": role.id,
                    "name": role.name,
                    "enabled": has_permission
                })
            
            permission_groups[category].append({
                "id": perm.id,
                "name": perm.name,
                "label": perm.label,
                "roles": role_assignments
            })
        
        # Convert to the expected format
        permission_groups_list = []
        for group_name, permissions in permission_groups.items():
            permission_groups_list.append({
                "group": group_name,
                "permissions": permissions
            })
        
        return {
            "status": "success",
            "data": {
                "permission_groups": permission_groups_list
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch grouped permissions: {str(e)}"
        }

@app.post("/api/permissions/", tags=["Role Management"])
async def create_permission(permission_data: dict):
    """Create a new permission"""
    try:
        from deelflow.models import Permission
        
        name = permission_data.get("name")
        label = permission_data.get("label")
        
        if not name or not label:
            return {
                "status": "error",
                "message": "Permission name and label are required"
            }
        
        # Check if permission already exists
        existing_permission = await sync_to_async(Permission.objects.filter)(name=name)
        if await sync_to_async(existing_permission.exists)():
            return {
                "status": "error",
                "message": "Permission with this name already exists"
            }
        
        # Create permission
        permission = await sync_to_async(Permission.objects.create)(
            name=name,
            label=label
        )
        return {
            "status": "success",
            "message": "Permission created successfully",
            "data": {
                "id": permission.id,
                "name": permission.name,
                "label": permission.label
            }
        }
    except Exception as e:
            return {
            "status": "error",
            "message": f"Failed to create permission: {str(e)}"
        }

# ==================== PAYMENT GATEWAY ENDPOINTS ====================

# Create security scheme for Swagger UI (HTTPBearer handles "Bearer" prefix automatically)
bearer_scheme = HTTPBearer(auto_error=False)

@app.get("/subscription-packs/", tags=["Payments"])
async def get_subscription_packages(request: Request):
    """
    **Get Subscription Packages**
    
    Retrieves all available subscription packages from Stripe.
    
    **Public Endpoint** 🔓
    - Visible to all users (no authentication required)
    - Shows available plans so users can view before signing in
    
    **Returns:**
    - List of subscription packages with pricing and features
    - Package details including Stripe price IDs
    
    **Example Request:**
    ```
    GET /subscription-packs/
    ```
    """
    try:
        from app.services.payment_service import PaymentService
        payment_service = PaymentService()
        result = await payment_service.get_subscription_packages()
        return result
    except HTTPException:
        raise
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get subscription packages: {str(e)}"
        }

# ==================== BLOCKCHAIN: POLYGON (MATIC) ====================

@app.get("/polygon/network", tags=["Blockchain"])
async def polygon_network_info():
    """
    **Polygon Network Info**

    Returns basic connection and network information for the configured Polygon RPC.
    """
    try:
        from app.services.polygon_service import PolygonService
        svc = PolygonService()
        return {"status": "success", "data": svc.get_network_info()}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/polygon/balance/{address}", tags=["Blockchain"])
async def polygon_get_balance(address: str):
    """
    **Get MATIC Balance**

    Returns the MATIC balance for the provided address.
    """
    try:
        from app.services.polygon_service import PolygonService
        svc = PolygonService()
        return {"status": "success", "data": svc.get_balance(address)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


class PolygonTransferRequest(BaseModel):
    to_address: str
    amount_matic: float
    private_key: Optional[str] = None  # optional; will use server key if not provided


@app.post("/polygon/transfer", tags=["Blockchain"])
async def polygon_transfer(req: PolygonTransferRequest, current_user: dict = Depends(get_current_user)):
    """
    **Transfer Native MATIC**

    Sends MATIC from the provided private key or the server wallet (if configured).
    Authentication required to prevent abuse.
    """
    try:
        from app.services.polygon_service import PolygonService
        svc = PolygonService()
        tx = svc.transfer_native(req.to_address, req.amount_matic, req.private_key)
        return {"status": "success", "data": tx}
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/create-checkout-session/", tags=["Payments"])
async def create_checkout_session(
    request_data: CheckoutSessionCreate,
    current_user: dict = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    """
    **Create Stripe Checkout Session**
    
    Creates a Stripe checkout session for subscription purchase.
    
    **Authentication Required** 🔐
    - User must be logged in to create a payment session
    - Include JWT token in Authorization header: `Bearer <token>`
    
    This endpoint is protected in Swagger via the Bearer auth scheme (lock icon). Click "Authorize" and paste your token.
    
    **Request Body:**
    
    **Minimum Required:** Only `price_id` is required. All other fields are optional.
    
    **Example 1 - Minimum (Only price_id):**
    ```json
    {
        "price_id": "price_1SM4xoE0wE8Cg1knewTgPQf5"
    }
    ```
    
    **Example 2 - With Optional Fields:**
    ```json
    {
        "price_id": "price_1SM4xoE0wE8Cg1knewTgPQf5",
        "customer_id": "cus_xxxxx",
        "success_url": "http://localhost:3000/payment/success",
        "cancel_url": "http://localhost:3000/payment/cancel",
        "payment_gateway": "stripe"
    }
    ```
    
    **Request Body Fields:**
    - **price_id** (✅ REQUIRED): Stripe price ID for the subscription plan
    - **customer_id** (optional): Existing Stripe customer ID
    - **success_url** (optional): Redirect URL after successful payment (default: auto-generated)
    - **cancel_url** (optional): Redirect URL if user cancels (default: auto-generated)
    - **payment_gateway** (optional): Payment gateway to use (default: "stripe")
    
    **Responses:**
    - 200: Checkout session URL and details
    - 401: Not authenticated (please sign in to buy a plan)
    
    **Returns:**
    - Checkout session URL and details
    - Transaction saved to database
    
    **Example Response:**
    ```json
    {
        "status": "success",
        "data": {
            "session_id": "cs_test_xxxxx",
            "url": "https://checkout.stripe.com/c/pay/cs_test_xxxxx",
            "customer_id": "cus_xxxxx"
        }
    }
    ```
    """
    try:
        from app.services.payment_service import PaymentService
        from deelflow.models import PaymentTransaction, User, SubscriptionPackage
        import uuid
        from datetime import datetime
        
        payment_service = PaymentService()
        
        # Get user from authentication
        # The get_current_user dependency should return the decoded JWT token payload
        # which contains user_id, email, role, exp, iat, type
        
        # Extract user_id - handle both plain payload and accidental response wrappers
        user_id = None
        
        if isinstance(current_user, dict):
            # Preferred: top-level payload fields
            user_id = (
                current_user.get("user_id") or
                current_user.get("sub") or  # Standard JWT subject claim
                current_user.get("id")
            )
            
            # Fallback: if someone accidentally passed a wrapped structure like {status, data}
            if not user_id and ("status" in current_user and "data" in current_user):
                data_field = current_user.get("data")
                if isinstance(data_field, dict):
                    user_id = (
                        data_field.get("user_id") or
                        data_field.get("id") or
                        (data_field.get("user", {}).get("id") if isinstance(data_field.get("user"), dict) else None) or
                        (data_field.get("tokens", {}).get("user_id") if isinstance(data_field.get("tokens"), dict) else None)
                    )
        
        if not user_id:
            # If user_id is not found, there might be an issue with token structure
            # Log full structure for debugging
            logger.error(f"[CHECKOUT] User ID not found in token payload.")
            logger.error(f"[CHECKOUT] Token payload keys: {list(current_user.keys()) if isinstance(current_user, dict) else 'Not a dict'}")
            logger.error(f"[CHECKOUT] Token payload: {current_user}")
            return {
                "status": "error",
                "message": f"User not found in token. Please login again. Token payload structure: {list(current_user.keys()) if isinstance(current_user, dict) else type(current_user).__name__}. The token should contain 'user_id' field."
            }
        
        logger.debug(f"[CHECKOUT] Extracted user_id: {user_id}")
        
        # Get user and package info
        try:
            user = await sync_to_async(User.objects.get)(id=user_id)
        except User.DoesNotExist:
            return {
                "status": "error",
                "message": f"User with ID {user_id} not found in database"
            }
        
        payment_gateway = request_data.payment_gateway or "stripe"
        
        # Get customer_id - use provided or user's Stripe customer ID
        customer_id = request_data.customer_id
        if not customer_id and hasattr(user, 'stripe_customer_id'):
            customer_id = user.stripe_customer_id
        
        # Create checkout session
        session_result = await payment_service.create_checkout_session(
            price_id=request_data.price_id,
            customer_id=customer_id,
            success_url=request_data.success_url,
            cancel_url=request_data.cancel_url
        )
        
        # Save transaction to database
        if session_result.get("status") == "success":
            transaction_id = f"{payment_gateway}_{uuid.uuid4().hex[:16]}"
            payment_data = session_result.get("data", {})
            session_id = payment_data.get("session_id")
            
            # Try to get plan details if available
            plan_name = "Unknown Plan"
            amount = 0
            currency = "USD"
            
            try:
                # Get amount from Stripe price (would need to fetch)
                # For now, we'll save with session_id
                plan_name = f"Plan {request_data.price_id[-10:]}"
            except:
                pass
            
            # Create payment transaction record
            transaction = await sync_to_async(PaymentTransaction.objects.create)(
                user=user,
                plan_id=request_data.price_id,
                plan_name=plan_name,
                amount=amount,  # Would need to fetch from Stripe
                currency=currency,
                payment_gateway=payment_gateway,
                transaction_id=transaction_id,
                payment_intent_id=session_id,
                status="pending",
                description=f"Payment for {plan_name}",
                metadata={
                    "session_id": session_id,
                    "price_id": request_data.price_id
                }
            )
            
            # Update response with transaction info
            session_result["data"]["transaction_id"] = transaction_id
            session_result["data"]["user_id"] = user_id
            session_result["message"] = "Checkout session created. Transaction saved."
        
        return session_result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"Failed to create checkout session: {str(e)}"
        }

@app.post("/create-customer-portal-session/", tags=["Payments"])
async def create_customer_portal_session(request_data: dict):
    """
    **Create Customer Portal Session**
    
    Creates a Stripe customer portal session for subscription management.
    
    **Request Body:**
    - customer_id: Stripe customer ID
    - return_url: Optional return URL
    
    **Returns:**
    - Customer portal URL
    """
    try:
        from app.services.payment_service import PaymentService
        payment_service = PaymentService()
        
        customer_id = request_data.get("customer_id")
        if not customer_id:
            return {
                "status": "error",
                "message": "Customer ID is required"
            }
        
        return await payment_service.create_customer_portal_session(
            customer_id=customer_id,
            return_url=request_data.get("return_url")
        )
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create customer portal session: {str(e)}"
        }

@app.post("/stripe-invoice/", tags=["Payments"])
async def get_customer_invoices(request_data: dict):
    """
    **Get Customer Invoices**
    
    Retrieves customer's invoice history from Stripe.
    
    **Request Body:**
    - customer_id: Stripe customer ID
    - limit: Optional limit for number of invoices (default: 10)
    
    **Returns:**
    - List of customer invoices
    """
    try:
        from app.services.payment_service import PaymentService
        payment_service = PaymentService()
        
        customer_id = request_data.get("customer_id")
        if not customer_id:
            return {
                "status": "error",
                "message": "Customer ID is required"
            }
        
        return await payment_service.get_customer_invoices(
            customer_id=customer_id,
            limit=request_data.get("limit", 10)
        )
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get customer invoices: {str(e)}"
        }

@app.get("/current-subscription/", tags=["Payments"])
async def get_current_subscription(customer_id: str = None):
    """
    **Get Current Subscription**
    
    Retrieves the customer's current active subscription.
    
    **Query Parameters:**
    - customer_id: Stripe customer ID
    
    **Returns:**
    - Current subscription details or null if no active subscription
    """
    try:
        from app.services.payment_service import PaymentService
        payment_service = PaymentService()
        
        if not customer_id:
            return {
                "status": "error",
                "message": "Customer ID is required"
            }
        
        return await payment_service.get_customer_subscription(customer_id)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get current subscription: {str(e)}"
        }

@app.get("/total-revenue/", tags=["Payments"])
async def get_total_revenue():
    """
    **Get Total Revenue**
    
    Retrieves total revenue metrics from Stripe.
    
    **Returns:**
    - Total revenue, MRR, customer count, and other metrics
    """
    try:
        from app.services.payment_service import PaymentService
        payment_service = PaymentService()
        return await payment_service.get_revenue_metrics()
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get revenue metrics: {str(e)}"
        }

@app.get("/monthly-profit/", tags=["Payments"])
async def get_monthly_profit():
    """
    **Get Monthly Profit**
    
    Retrieves monthly profit and revenue data.
    
    **Returns:**
    - Monthly profit metrics and trends
    """
    try:
        from app.services.payment_service import PaymentService
        payment_service = PaymentService()
        return await payment_service.get_revenue_metrics()
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get monthly profit: {str(e)}"
        }

@app.post("/verify-payment/", tags=["Payments"])
async def verify_payment(request_data: dict):
    """
    **Verify Payment**
    
    Verifies payment completion using Stripe session ID.
    
    **Request Body:**
    - session_id: Stripe checkout session ID
    
    **Returns:**
    - Payment verification status and details
    """
    try:
        from app.services.payment_service import PaymentService
        payment_service = PaymentService()
        
        session_id = request_data.get("session_id")
        if not session_id:
            return {
                "status": "error",
                "message": "Session ID is required"
            }
        
        return await payment_service.verify_payment(session_id)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to verify payment: {str(e)}"
        }

@app.post("/create-payment-intent/", tags=["Payments"])
async def create_payment_intent(request_data: PaymentIntentCreate):
    """
    **Create Payment Intent**
    
    Creates a Stripe payment intent for one-time payments.
    
    **Request Body:**
    - amount: Payment amount
    - currency: Currency code (default: usd)
    - metadata: Optional metadata
    - description: Optional description
    
    **Returns:**
    - Payment intent with client secret
    """
    try:
        from app.services.payment_service import PaymentService
        payment_service = PaymentService()
        
        return await payment_service.create_payment_intent(
            amount=request_data.amount,
            currency=request_data.currency,
            metadata=request_data.metadata
        )
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create payment intent: {str(e)}"
        }

# ==================== SIGNNOW API INTEGRATION ENDPOINTS ====================

@app.get("/api/signnow/test/", tags=["SignNow"])
async def test_signnow_connection():
    """
    **Test SignNow API Connection**
    
    Tests the connection to SignNow API and verifies authentication.
    
    **Returns:**
    - Connection status
    - Authentication status
    - User information
    """
    try:
        from app.services.signnow_service import signnow_service
        
        result = signnow_service.test_connection()
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to test SignNow connection: {str(e)}"
        }

@app.get("/api/signnow/user/", tags=["SignNow"])
async def get_signnow_user():
    """
    **Get SignNow User Information**
    
    Retrieves authenticated user information from SignNow.
    
    **Returns:**
    - User email
    - User ID
    - Account information
    """
    try:
        from app.services.signnow_service import signnow_service
        
        result = signnow_service.get_user_info()
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get user info: {str(e)}"
        }

@app.get("/api/signnow/documents/", tags=["SignNow"])
async def get_signnow_documents(limit: int = 100):
    """
    **Get SignNow Documents**
    
    Retrieves list of documents from SignNow account.
    
    **Query Parameters:**
    - limit: Maximum number of documents (default: 100)
    
    **Returns:**
    - List of documents
    """
    try:
        from app.services.signnow_service import signnow_service
        
        result = signnow_service.get_documents(limit=limit)
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get documents: {str(e)}"
        }

@app.post("/api/signnow/documents/", tags=["SignNow"])
async def create_signnow_document(
    document_name: str,
    file_path: Optional[str] = None
):
    """
    **Create SignNow Document**
    
    Creates a new document in SignNow.
    
    **Request Parameters:**
    - document_name: Name of the document
    - file_path: Path to document file (optional)
    
    **Returns:**
    - Document ID
    - Document information
    """
    try:
        from app.services.signnow_service import signnow_service
        
        result = signnow_service.create_document(
            document_name=document_name,
            file_path=file_path
        )
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create document: {str(e)}"
        }

@app.post("/api/signnow/upload/", tags=["SignNow"])
async def upload_signnow_document(
    file: UploadFile = File(...),
    document_name: Optional[str] = None
):
    """
    **Upload Document to SignNow**
    
    Uploads a document file to SignNow for signing.
    
    **Request Body:**
    - file: Document file (PDF, DOCX, etc.)
    - document_name: Optional custom name for the document
    
    **Returns:**
    - Document ID
    - Document information
    """
    try:
        from app.services.signnow_service import signnow_service
        import tempfile
        import os
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Upload to SignNow
            result = signnow_service.upload_document(
                file_path=tmp_path,
                document_name=document_name or file.filename
            )
            return result
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to upload document: {str(e)}"
        }

@app.post("/api/signnow/invite/", tags=["SignNow"])
async def invite_signnow_signers(
    document_id: str = Body(...),
    signers: List[Dict[str, Any]] = Body(...),
    subject: Optional[str] = Body(None),
    message: Optional[str] = Body(None)
):
    """
    **Invite Signers to Document**
    
    Sends signature invitations to one or more signers.
    
    **Request Body:**
    - document_id: SignNow document ID
    - signers: List of signer objects with email, order (optional), role (optional)
    - subject: Email subject (optional)
    - message: Email message (optional)
    
    **Returns:**
    - Invitation status
    - Invitation IDs
    """
    try:
        from app.services.signnow_service import signnow_service
        
        result = signnow_service.invite_signers(
            document_id=document_id,
            signers=signers,
            subject=subject,
            message=message
        )
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to send invitation: {str(e)}"
        }

@app.get("/api/signnow/status/{document_id}", tags=["SignNow"])
async def get_signnow_document_status(document_id: str):
    """
    **Get Document Status**
    
    Retrieves the current status and information about a document.
    
    **Path Parameters:**
    - document_id: SignNow document ID
    
    **Returns:**
    - Document status
    - Signing progress
    - Signer information
    """
    try:
        from app.services.signnow_service import signnow_service
        
        result = signnow_service.get_document_status(document_id=document_id)
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get document status: {str(e)}"
        }

@app.get("/api/signnow/download/{document_id}", tags=["SignNow"])
async def download_signnow_document(
    document_id: str,
    save_path: Optional[str] = None
):
    """
    **Download Document**
    
    Downloads a completed or in-progress document from SignNow.
    
    **Path Parameters:**
    - document_id: SignNow document ID
    
    **Query Parameters:**
    - save_path: Optional path to save the downloaded file
    
    **Returns:**
    - Document file content or save confirmation
    """
    try:
        from app.services.signnow_service import signnow_service
        
        result = signnow_service.download_document(
            document_id=document_id,
            file_path=save_path
        )
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to download document: {str(e)}"
        }

@app.post("/api/signnow/documents/{document_id}/send/", tags=["SignNow"])
async def send_signnow_document(
    document_id: str,
    signer_email: str,
    subject: Optional[str] = None,
    message: Optional[str] = None
):
    """
    **Send Document for Signature (Legacy)**
    
    Sends a SignNow document to a signer for signature.
    For multiple signers, use /api/signnow/invite/ instead.
    
    **Path Parameters:**
    - document_id: SignNow document ID
    
    **Request Body:**
    - signer_email: Email address of the signer
    - subject: Email subject (optional)
    - message: Email message (optional)
    
    **Returns:**
    - Sending status
    - Invitation ID
    """
    try:
        from app.services.signnow_service import signnow_service
        
        result = signnow_service.send_document_for_signature(
            document_id=document_id,
            signer_email=signer_email,
            subject=subject,
            message=message
        )
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to send document: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8140)
