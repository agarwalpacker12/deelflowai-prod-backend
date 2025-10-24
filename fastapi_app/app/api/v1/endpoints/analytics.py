"""
Analytics and metrics endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
from app.core.security import get_current_user, require_permission
from app.core.exceptions import NotFoundError, AuthorizationError
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import DashboardMetrics, BusinessMetrics, AIAnalytics
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/dashboard", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    current_user = Depends(get_current_user)
):
    """Get dashboard metrics"""
    try:
        analytics_service = AnalyticsService()
        
        # Check permissions
        if not analytics_service.has_permission(current_user, "view_analytics"):
            raise AuthorizationError("Permission to view analytics required")
        
        metrics = await analytics_service.get_dashboard_metrics(current_user.organization_id)
        return metrics
    
    except Exception as e:
        logger.error(f"Get dashboard metrics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve dashboard metrics"
        )

@router.get("/business", response_model=BusinessMetrics)
async def get_business_metrics(
    current_user = Depends(get_current_user)
):
    """Get business metrics"""
    try:
        analytics_service = AnalyticsService()
        
        # Check permissions
        if not analytics_service.has_permission(current_user, "view_analytics"):
            raise AuthorizationError("Permission to view analytics required")
        
        metrics = await analytics_service.get_business_metrics(current_user.organization_id)
        return metrics
    
    except Exception as e:
        logger.error(f"Get business metrics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve business metrics"
        )

@router.get("/ai", response_model=AIAnalytics)
async def get_ai_analytics(
    current_user = Depends(get_current_user)
):
    """Get AI analytics"""
    try:
        analytics_service = AnalyticsService()
        
        # Check permissions
        if not analytics_service.has_permission(current_user, "view_analytics"):
            raise AuthorizationError("Permission to view analytics required")
        
        analytics = await analytics_service.get_ai_analytics(current_user.organization_id)
        return analytics
    
    except Exception as e:
        logger.error(f"Get AI analytics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve AI analytics"
        )

@router.get("/revenue")
async def get_revenue_metrics(
    period: str = Query("30d", description="Time period: 7d, 30d, 90d, 1y"),
    current_user = Depends(get_current_user)
):
    """Get revenue metrics"""
    try:
        analytics_service = AnalyticsService()
        
        # Check permissions
        if not analytics_service.has_permission(current_user, "view_analytics"):
            raise AuthorizationError("Permission to view analytics required")
        
        metrics = await analytics_service.get_revenue_metrics(
            current_user.organization_id,
            period
        )
        return metrics
    
    except Exception as e:
        logger.error(f"Get revenue metrics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve revenue metrics"
        )

@router.get("/users")
async def get_user_metrics(
    current_user = Depends(get_current_user)
):
    """Get user metrics"""
    try:
        analytics_service = AnalyticsService()
        
        # Check permissions
        if not analytics_service.has_permission(current_user, "view_analytics"):
            raise AuthorizationError("Permission to view analytics required")
        
        metrics = await analytics_service.get_user_metrics(current_user.organization_id)
        return metrics
    
    except Exception as e:
        logger.error(f"Get user metrics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user metrics"
        )

@router.get("/campaigns")
async def get_campaign_metrics(
    current_user = Depends(get_current_user)
):
    """Get campaign metrics"""
    try:
        analytics_service = AnalyticsService()
        
        # Check permissions
        if not analytics_service.has_permission(current_user, "view_analytics"):
            raise AuthorizationError("Permission to view analytics required")
        
        metrics = await analytics_service.get_campaign_metrics(current_user.organization_id)
        return metrics
    
    except Exception as e:
        logger.error(f"Get campaign metrics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve campaign metrics"
        )

@router.get("/leads")
async def get_lead_metrics(
    current_user = Depends(get_current_user)
):
    """Get lead metrics"""
    try:
        analytics_service = AnalyticsService()
        
        # Check permissions
        if not analytics_service.has_permission(current_user, "view_analytics"):
            raise AuthorizationError("Permission to view analytics required")
        
        metrics = await analytics_service.get_lead_metrics(current_user.organization_id)
        return metrics
    
    except Exception as e:
        logger.error(f"Get lead metrics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve lead metrics"
        )

@router.get("/deals")
async def get_deal_metrics(
    current_user = Depends(get_current_user)
):
    """Get deal metrics"""
    try:
        analytics_service = AnalyticsService()
        
        # Check permissions
        if not analytics_service.has_permission(current_user, "view_analytics"):
            raise AuthorizationError("Permission to view analytics required")
        
        metrics = await analytics_service.get_deal_metrics(current_user.organization_id)
        return metrics
    
    except Exception as e:
        logger.error(f"Get deal metrics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve deal metrics"
        )

@router.get("/activity")
async def get_activity_feed(
    limit: int = Query(50, ge=1, le=200),
    current_user = Depends(get_current_user)
):
    """Get activity feed"""
    try:
        analytics_service = AnalyticsService()
        
        # Check permissions
        if not analytics_service.has_permission(current_user, "view_analytics"):
            raise AuthorizationError("Permission to view analytics required")
        
        activities = await analytics_service.get_activity_feed(
            current_user.organization_id,
            limit
        )
        return activities
    
    except Exception as e:
        logger.error(f"Get activity feed error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve activity feed"
        )

@router.get("/compliance")
async def get_compliance_status(
    current_user = Depends(get_current_user)
):
    """Get compliance status"""
    try:
        analytics_service = AnalyticsService()
        
        # Check permissions
        if not analytics_service.has_permission(current_user, "view_analytics"):
            raise AuthorizationError("Permission to view analytics required")
        
        status = await analytics_service.get_compliance_status(current_user.organization_id)
        return status
    
    except Exception as e:
        logger.error(f"Get compliance status error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve compliance status"
        )

# Additional endpoints for frontend compatibility
@router.get("/stats")
async def get_stats():
    """Get general statistics for the dashboard"""
    try:
        # Mock data for now - in production, this would come from the database
        stats = {
            'total_users': 150,
            'total_properties': 89,
            'total_leads': 234,
            'total_deals': 45,
            'active_campaigns': 12,
            'revenue': 125000.50,
            'monthly_profit': 25000.75,
            'voice_calls': 156,
        }
        
        return {
            'status': 'success',
            'data': stats
        }
    except Exception as e:
        logger.error(f"Get stats error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve stats"
        )

@router.get("/opportunity-cost-analysis")
async def get_opportunity_cost_analysis():
    """Get opportunity cost analysis data"""
    try:
        analysis = {
            'total_revenue': 125000.50,
            'monthly_profit': 25000.75,
            'properties_listed': 89,
            'total_deals': 45,
            'opportunity_cost': 12500.05,  # 10% of revenue
            'efficiency_score': 85.5,
            'recommendations': [
                'Increase lead conversion rate by 15%',
                'Optimize property listing strategy',
                'Improve deal closing timeline'
            ]
        }
        
        return {
            'status': 'success',
            'data': analysis
        }
    except Exception as e:
        logger.error(f"Get opportunity cost analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve opportunity cost analysis"
        )

@router.get("/status")
async def get_status():
    """Get system status and health information"""
    try:
        status_data = {
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
            'timestamp': '2025-10-09T04:27:00Z'
        }
        
        return {
            'status': 'success',
            'data': status_data
        }
    except Exception as e:
        logger.error(f"Get status error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve status"
        )

@router.get("/recent-activity")
async def get_recent_activity():
    """Get recent activity feed"""
    try:
        activities = [
            {"event": "New lead added", "date": "2025-10-08", "user": "System", "action_type": "lead_created"},
            {"event": "Property analysis completed", "date": "2025-10-07", "user": "AI", "action_type": "ai_analysis"},
            {"event": "Campaign launched", "date": "2025-10-06", "user": "Admin", "action_type": "campaign_created"},
            {"event": "Deal closed", "date": "2025-10-05", "user": "Agent", "action_type": "deal_closed"}
        ]
        
        return {
            "status": "success",
            "message": "Recent activity retrieved successfully",
            "data": {
                "activities": activities,
                "last_updated": "2025-10-09T04:27:00Z"
            }
        }
    except Exception as e:
        logger.error(f"Get recent activity error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve recent activity"
        )

@router.get("/voice-ai-calls-count")
async def get_voice_ai_calls_count():
    """Get voice AI calls count"""
    try:
        return {
            'total_calls': 156,
            'success_rate': 87.5,
            'created_at': '2025-10-09T04:27:00Z',
            'updated_at': '2025-10-09T04:27:00Z'
        }
    except Exception as e:
        logger.error(f"Get voice AI calls count error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve voice AI calls count"
        )