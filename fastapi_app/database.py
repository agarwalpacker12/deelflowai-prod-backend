"""
Database connection and query functions for FastAPI
"""

import os
import sys
import django
from pathlib import Path
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from typing import Dict, List, Any, Optional
from asgiref.sync import sync_to_async

# Add Django project to Python path
django_project_path = Path(__file__).resolve().parent.parent
sys.path.append(str(django_project_path))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deelflow.settings')
django.setup()

# Import Django models
from deelflow.models import (
    User, Organization, Lead, Property, Deal, AIAnalysis, 
    BusinessMetrics, PropertyAIAnalysis, VisionAnalysisMetrics,
    VoiceAICallMetrics, BlockchainTxnMetrics, NLPProcessingMetrics,
    Campaign, CampaignPerformance, CampaignPropertyStats,
    DiscoveredLead, OutreachCampaign, CampaignRecipient
)

async def _get_dashboard_stats_sync() -> Dict[str, Any]:
    """Async version of get_dashboard_stats"""
    try:
        # Get counts from database
        total_properties = await sync_to_async(Property.objects.count)()
        total_leads = await sync_to_async(Lead.objects.count)()
        total_deals = await sync_to_async(Deal.objects.count)()
        total_users = await sync_to_async(User.objects.count)()
        
        # Get recent activity
        recent_properties = await sync_to_async(Property.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count)()
        
        recent_leads = await sync_to_async(Lead.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count)()
        
        recent_deals = await sync_to_async(Deal.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count)()
        
        return {
            "totalProperties": total_properties,
            "totalLeads": total_leads,
            "totalDeals": total_deals,
            "totalUsers": total_users,
            "recentProperties": recent_properties,
            "recentLeads": recent_leads,
            "recentDeals": recent_deals,
            "lastUpdated": timezone.now().isoformat()
        }
    except Exception as e:
        print(f"Error getting dashboard stats: {e}")
        return {
            "totalProperties": 0,
            "totalLeads": 0,
            "totalDeals": 0,
            "totalUsers": 0,
            "recentProperties": 0,
            "recentLeads": 0,
            "recentDeals": 0,
            "lastUpdated": timezone.now().isoformat()
        }

# Async wrapper
get_dashboard_stats = _get_dashboard_stats_sync

def _get_ai_metrics_sync() -> Dict[str, Any]:
    """Synchronous version of get_ai_metrics"""
    try:
        # Get AI analysis data
        total_analyses = AIAnalysis.objects.count()
        property_analyses = PropertyAIAnalysis.objects.count()
        vision_analyses = VisionAnalysisMetrics.objects.count()
        voice_calls = VoiceAICallMetrics.objects.count()
        nlp_analyses = NLPProcessingMetrics.objects.count()
        blockchain_txns = BlockchainTxnMetrics.objects.count()
        
        # Calculate accuracy (mock for now)
        avg_accuracy = 92.5 if total_analyses > 0 else 0
        
        return {
            "totalAnalyses": total_analyses,
            "propertyAnalyses": property_analyses,
            "visionAnalyses": vision_analyses,
            "voiceCalls": voice_calls,
            "nlpAnalyses": nlp_analyses,
            "blockchainTxns": blockchain_txns,
            "avgAccuracy": avg_accuracy,
            "lastUpdated": timezone.now().isoformat()
        }
    except Exception as e:
        print(f"Error getting AI metrics: {e}")
        return {
            "totalAnalyses": 0,
            "propertyAnalyses": 0,
            "visionAnalyses": 0,
            "voiceCalls": 0,
            "nlpAnalyses": 0,
            "blockchainTxns": 0,
            "avgAccuracy": 0,
            "lastUpdated": timezone.now().isoformat()
        }

# Async wrapper
get_ai_metrics = sync_to_async(_get_ai_metrics_sync)

def _get_tenant_management_data_sync() -> Dict[str, Any]:
    """Synchronous version of get_tenant_management_data"""
    try:
        # Get organization data
        total_organizations = Organization.objects.count()
        # Use subscription_status to determine active organizations
        active_organizations = Organization.objects.exclude(subscription_status='suspended').count()
        
        # Mock tenant data (since we don't have tenant model yet)
        return {
            "activeTenants": str(active_organizations),
            "paymentOverdue": "0",
            "suspended": "0",
            "monthlyRevenue": f"${total_organizations * 1000}"
        }
    except Exception as e:
        print(f"Error getting tenant management data: {e}")
        return {
            "activeTenants": "0",
            "paymentOverdue": "0",
            "suspended": "0",
            "monthlyRevenue": "$0"
        }

# Async wrapper
get_tenant_management_data = sync_to_async(_get_tenant_management_data_sync)

def _get_opportunity_cost_data_sync() -> Dict[str, Any]:
    """Synchronous version of get_opportunity_cost_data"""
    try:
        # Get deal data
        total_deals = Deal.objects.count()
        closed_deals = Deal.objects.filter(status='closed').count()
        pending_deals = Deal.objects.filter(status='pending').count()
        
        # Calculate potential revenue
        total_revenue = sum([deal.final_price or 0 for deal in Deal.objects.filter(status='closed')])
        potential_revenue = sum([deal.offer_price or 0 for deal in Deal.objects.filter(status='pending')])
        
        return {
            "lostRevenue": float(total_revenue) * 0.1,  # 10% of closed deals
            "lostRevenueDescription": "Revenue lost due to delayed deal closures and missed opportunities",
            "potentialRevenue": float(potential_revenue),
            "currentRevenue": float(total_revenue),
            "projectedRevenue": float(total_revenue) * 1.2,
            "optimizationNeeded": "Lead conversion process and property listing strategy",
            "roiConversionEfficiency": 78.5,
            "peakTimeMonths": ["March", "April", "May", "September", "October"],
            "peakDescription": "Spring and fall seasons show highest property activity and deal closures"
        }
    except Exception as e:
        print(f"Error getting opportunity cost data: {e}")
        return {
            "lostRevenue": 0.0,
            "lostRevenueDescription": "No data available",
            "potentialRevenue": 0.0,
            "currentRevenue": 0.0,
            "projectedRevenue": 0.0,
            "optimizationNeeded": "Data collection needed",
            "roiConversionEfficiency": 0.0,
            "peakTimeMonths": [],
            "peakDescription": "No data available"
        }

# Async wrapper
get_opportunity_cost_data = sync_to_async(_get_opportunity_cost_data_sync)

def _get_revenue_growth_data_sync() -> Dict[str, Any]:
    """Synchronous version of get_revenue_growth_data"""
    try:
        # Get deal data for last 6 months
        six_months_ago = timezone.now() - timedelta(days=180)
        recent_deals = Deal.objects.filter(
            created_at__gte=six_months_ago,
            status='closed'
        )
        
        monthly_revenue = []
        for i in range(6):
            month_start = timezone.now() - timedelta(days=30*(i+1))
            month_end = timezone.now() - timedelta(days=30*i)
            month_deals = recent_deals.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            )
            monthly_revenue.append(sum([deal.final_price or 0 for deal in month_deals]))
        
        monthly_revenue.reverse()  # Oldest to newest
        
        return {
            "revenueData": [float(r) for r in monthly_revenue],
            "userData": [User.objects.filter(created_at__gte=timezone.now() - timedelta(days=30*i)).count() for i in range(6, 0, -1)],
            "labels": ["6m ago", "5m ago", "4m ago", "3m ago", "2m ago", "1m ago"]
        }
    except Exception as e:
        print(f"Error getting revenue growth data: {e}")
        return {
            "revenueData": [0, 0, 0, 0, 0, 0],
            "userData": [0, 0, 0, 0, 0, 0],
            "labels": ["6m ago", "5m ago", "4m ago", "3m ago", "2m ago", "1m ago"]
        }

# Async wrapper
get_revenue_growth_data = sync_to_async(_get_revenue_growth_data_sync)

def _get_market_alerts_data_sync() -> List[Dict[str, Any]]:
    """Synchronous version of get_market_alerts_data"""
    try:
        # Get recent property and deal activity
        recent_properties = Property.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).order_by('-created_at')[:5]
        
        alerts = []
        for prop in recent_properties:
            alerts.append({
                "id": prop.id,
                "type": "new_property",
                "message": f"New property listed: {prop.address}",
                "timestamp": prop.created_at.isoformat()
            })
        
        # If no recent properties, return some sample alerts
        if not alerts:
            alerts = [
                {
                    "id": "alert_1",
                    "type": "market_trend",
                    "message": "Property prices in downtown area increased by 5.2% this week",
                    "timestamp": timezone.now().isoformat()
                },
                {
                    "id": "alert_2", 
                    "type": "opportunity",
                    "message": "New distressed property opportunity in Miami - 20% below market value",
                    "timestamp": (timezone.now() - timedelta(hours=2)).isoformat()
                },
                {
                    "id": "alert_3",
                    "type": "market_alert",
                    "message": "Interest rates dropped to 6.8% - great time for buyers",
                    "timestamp": (timezone.now() - timedelta(hours=6)).isoformat()
                }
            ]
        
        return alerts
    except Exception as e:
        print(f"Error getting market alerts data: {e}")
        return []

# Async wrapper
get_market_alerts_data = sync_to_async(_get_market_alerts_data_sync)

def _get_live_activity_data_sync() -> List[Dict[str, Any]]:
    """Synchronous version of get_live_activity_data"""
    try:
        # Get recent activity from various models
        activities = []
        
        # Recent properties
        recent_properties = Property.objects.filter(
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).order_by('-created_at')[:3]
        
        for prop in recent_properties:
            activities.append({
                "id": f"prop_{prop.id}",
                "type": "property_viewed",
                "message": f"Property {prop.address} viewed by lead",
                "timestamp": prop.created_at.isoformat()
            })
        
        # Recent deals
        recent_deals = Deal.objects.filter(
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).order_by('-created_at')[:2]
        
        for deal in recent_deals:
            activities.append({
                "id": f"deal_{deal.id}",
                "type": "deal_updated",
                "message": f"Deal #{deal.id} status updated to '{deal.status}'",
                "timestamp": deal.created_at.isoformat()
            })
        
        # If no recent activity, return some sample activities
        if not activities:
            activities = [
                {
                    "id": "activity_1",
                    "type": "lead_activity",
                    "message": "New lead Sarah Johnson viewed property at 123 Main Street",
                    "timestamp": timezone.now().isoformat()
                },
                {
                    "id": "activity_2",
                    "type": "deal_activity", 
                    "message": "Deal #1234 moved to 'Under Contract' status",
                    "timestamp": (timezone.now() - timedelta(minutes=30)).isoformat()
                },
                {
                    "id": "activity_3",
                    "type": "ai_activity",
                    "message": "AI analyzed 15 properties and identified 3 high-potential deals",
                    "timestamp": (timezone.now() - timedelta(hours=1)).isoformat()
                },
                {
                    "id": "activity_4",
                    "type": "campaign_activity",
                    "message": "Email campaign 'Q4 Properties' sent to 150 leads",
                    "timestamp": (timezone.now() - timedelta(hours=2)).isoformat()
                }
            ]
        
        return sorted(activities, key=lambda x: x['timestamp'], reverse=True)
    except Exception as e:
        print(f"Error getting live activity data: {e}")
        return []

# Async wrapper
get_live_activity_data = sync_to_async(_get_live_activity_data_sync)

def _get_performance_metrics_sync() -> Dict[str, Any]:
    """Synchronous version of get_performance_metrics"""
    try:
        # Get business metrics
        business_metrics = BusinessMetrics.objects.first()
        
        if business_metrics:
            return {
                "totalRevenue": float(business_metrics.total_revenue or 0),
                "totalLeads": business_metrics.total_leads or 0,
                "totalDeals": business_metrics.total_deals or 0,
                "aiConversations": business_metrics.ai_conversations or 0,
                "conversionRate": float(business_metrics.conversion_rate or 0),
                "avgDealSize": float(business_metrics.avg_deal_size or 0),
                "lastUpdated": timezone.now().isoformat()
            }
        else:
            return {
                "totalRevenue": 0.0,
                "totalLeads": 0,
                "totalDeals": 0,
                "aiConversations": 0,
                "conversionRate": 0.0,
                "avgDealSize": 0.0,
                "lastUpdated": timezone.now().isoformat()
            }
    except Exception as e:
        print(f"Error getting performance metrics: {e}")
        return {
            "totalRevenue": 0.0,
            "totalLeads": 0,
            "totalDeals": 0,
            "aiConversations": 0,
            "conversionRate": 0.0,
            "avgDealSize": 0.0,
            "lastUpdated": timezone.now().isoformat()
        }

# Async wrapper
get_performance_metrics = sync_to_async(_get_performance_metrics_sync)
