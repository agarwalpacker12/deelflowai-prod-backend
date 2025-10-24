"""
Analytics service for business logic
"""

from typing import Dict, Any, List
from decimal import Decimal
from datetime import datetime, timedelta
from app.core.exceptions import NotFoundError, ValidationError
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Analytics service class"""
    
    def __init__(self):
        self.django_models = {}
        self._setup_django_models()
    
    def _setup_django_models(self):
        """Setup Django models"""
        try:
            import django
            from django.apps import apps
            
            self.django_models = {
                'business_metrics': apps.get_model('deelflow', 'BusinessMetrics'),
                'historical_metrics': apps.get_model('deelflow', 'HistoricalMetrics'),
                'activity_feed': apps.get_model('deelflow', 'ActivityFeed'),
                'compliance_status': apps.get_model('deelflow', 'ComplianceStatus'),
                'user': apps.get_model('deelflow', 'User'),
                'property': apps.get_model('deelflow', 'Property'),
                'lead': apps.get_model('deelflow', 'Lead'),
                'deal': apps.get_model('deelflow', 'Deal'),
                'campaign': apps.get_model('deelflow', 'Campaign')
            }
        except Exception as e:
            logger.error(f"Failed to setup Django models: {e}")
    
    async def get_dashboard_metrics(self, organization_id: int) -> Dict[str, Any]:
        """Get dashboard metrics"""
        try:
            # Get latest business metrics
            business_metrics = self.django_models['business_metrics'].objects.latest('report_date')
            
            # Get compliance status
            compliance = self.django_models['compliance_status'].objects.latest('updated_at')
            
            return {
                "total_revenue": business_metrics.total_revenue,
                "active_users": business_metrics.active_users,
                "total_properties": business_metrics.properties_listed,
                "total_leads": business_metrics.total_deals,  # Using total_deals as proxy for leads
                "total_deals": business_metrics.total_deals,
                "monthly_profit": business_metrics.monthly_profit,
                "voice_calls_count": business_metrics.voice_calls_count,
                "ai_conversations": business_metrics.ai_conversations,
                "compliance_percentage": compliance.compliance_percent,
                "system_health": compliance.system_health,
                "last_updated": business_metrics.report_date
            }
        except Exception as e:
            logger.error(f"Error getting dashboard metrics: {e}")
            raise
    
    async def get_business_metrics(self, organization_id: int) -> Dict[str, Any]:
        """Get business metrics"""
        try:
            # Get historical data for trends
            historical_data = self.django_models['historical_metrics'].objects.all()[:30]
            
            # Calculate growth rates
            revenue_growth = self._calculate_growth_rate(historical_data, 'revenue')
            user_growth = self._calculate_growth_rate(historical_data, 'active_users')
            
            return {
                "revenue_growth": revenue_growth,
                "user_growth": user_growth,
                "property_growth": 0.0,  # Placeholder
                "lead_conversion_rate": 0.0,  # Placeholder
                "deal_success_rate": 0.0,  # Placeholder
                "profit_margin": 0.0,  # Placeholder
                "customer_satisfaction": 0.0,  # Placeholder
                "market_share": 0.0  # Placeholder
            }
        except Exception as e:
            logger.error(f"Error getting business metrics: {e}")
            raise
    
    async def get_ai_analytics(self, organization_id: int) -> Dict[str, Any]:
        """Get AI analytics"""
        try:
            # Get AI metrics from various models
            vision_metrics = self.django_models['vision'].objects.latest('updated_at')
            nlp_metrics = self.django_models['nlp'].objects.latest('updated_at')
            voice_metrics = self.django_models['voice'].objects.latest('updated_at')
            blockchain_metrics = self.django_models['blockchain'].objects.latest('updated_at')
            
            return {
                "vision_accuracy": vision_metrics.accuracy_rate,
                "nlp_accuracy": nlp_metrics.accuracy_rate,
                "voice_success_rate": voice_metrics.success_rate,
                "blockchain_success_rate": blockchain_metrics.success_rate,
                "overall_ai_performance": (
                    vision_metrics.accuracy_rate + 
                    nlp_metrics.accuracy_rate + 
                    voice_metrics.success_rate + 
                    blockchain_metrics.success_rate
                ) / 4,
                "ai_usage_trends": {},  # Placeholder
                "cost_per_analysis": Decimal('0.50'),  # Placeholder
                "roi_from_ai": 0.0  # Placeholder
            }
        except Exception as e:
            logger.error(f"Error getting AI analytics: {e}")
            raise
    
    async def get_revenue_metrics(self, organization_id: int, period: str) -> Dict[str, Any]:
        """Get revenue metrics"""
        try:
            # Calculate date range based on period
            end_date = datetime.now()
            if period == "7d":
                start_date = end_date - timedelta(days=7)
            elif period == "30d":
                start_date = end_date - timedelta(days=30)
            elif period == "90d":
                start_date = end_date - timedelta(days=90)
            elif period == "1y":
                start_date = end_date - timedelta(days=365)
            else:
                start_date = end_date - timedelta(days=30)
            
            # Get revenue data
            revenue_data = self.django_models['historical_metrics'].objects.filter(
                metric_type='revenue',
                record_date__range=[start_date, end_date]
            )
            
            total_revenue = sum(item.metric_value for item in revenue_data)
            
            return {
                "period": period,
                "total_revenue": total_revenue,
                "revenue_growth": 0.0,  # Placeholder
                "revenue_by_source": {},  # Placeholder
                "monthly_breakdown": [],  # Placeholder
                "projected_revenue": total_revenue * 1.1  # Placeholder
            }
        except Exception as e:
            logger.error(f"Error getting revenue metrics: {e}")
            raise
    
    async def get_user_metrics(self, organization_id: int) -> Dict[str, Any]:
        """Get user metrics"""
        try:
            users = self.django_models['user'].objects.filter(organization_id=organization_id)
            
            return {
                "total_users": users.count(),
                "active_users": users.filter(is_active=True).count(),
                "new_users": users.filter(created_at__gte=datetime.now() - timedelta(days=30)).count(),
                "user_retention": 0.0,  # Placeholder
                "users_by_role": {},  # Placeholder
                "user_activity": []  # Placeholder
            }
        except Exception as e:
            logger.error(f"Error getting user metrics: {e}")
            raise
    
    async def get_campaign_metrics(self, organization_id: int) -> Dict[str, Any]:
        """Get campaign metrics"""
        try:
            campaigns = self.django_models['campaign'].objects.filter(
                created_by__organization_id=organization_id
            )
            
            return {
                "total_campaigns": campaigns.count(),
                "active_campaigns": campaigns.filter(status='active').count(),
                "completed_campaigns": campaigns.filter(status='completed').count(),
                "total_leads_generated": 0,  # Placeholder
                "conversion_rate": 0.0,  # Placeholder
                "roi_percentage": 0.0,  # Placeholder
                "cost_per_lead": Decimal('0.00'),  # Placeholder
                "revenue_generated": Decimal('0.00')  # Placeholder
            }
        except Exception as e:
            logger.error(f"Error getting campaign metrics: {e}")
            raise
    
    async def get_lead_metrics(self, organization_id: int) -> Dict[str, Any]:
        """Get lead metrics"""
        try:
            leads = self.django_models['lead'].objects.all()  # Assuming leads are global
            
            return {
                "total_leads": leads.count(),
                "new_leads": leads.filter(status='new').count(),
                "qualified_leads": leads.filter(status='qualified').count(),
                "converted_leads": leads.filter(status='converted').count(),
                "conversion_rate": 0.0,  # Placeholder
                "leads_by_source": {},  # Placeholder
                "average_lead_value": Decimal('0.00'),  # Placeholder
                "lead_quality_score": 0.0  # Placeholder
            }
        except Exception as e:
            logger.error(f"Error getting lead metrics: {e}")
            raise
    
    async def get_deal_metrics(self, organization_id: int) -> Dict[str, Any]:
        """Get deal metrics"""
        try:
            deals = self.django_models['deal'].objects.all()  # Assuming deals are global
            
            return {
                "total_deals": deals.count(),
                "pending_deals": deals.filter(status='pending').count(),
                "closed_deals": deals.filter(status='closed').count(),
                "total_deal_value": Decimal('0.00'),  # Placeholder
                "average_deal_value": Decimal('0.00'),  # Placeholder
                "deal_success_rate": 0.0,  # Placeholder
                "deals_by_type": {},  # Placeholder
                "monthly_deals": []  # Placeholder
            }
        except Exception as e:
            logger.error(f"Error getting deal metrics: {e}")
            raise
    
    async def get_activity_feed(self, organization_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get activity feed"""
        try:
            activities = self.django_models['activity_feed'].objects.all()[:limit]
            
            return [
                {
                    "id": activity.id,
                    "user_id": activity.user_id,
                    "action_type": activity.action_type,
                    "description": activity.description,
                    "timestamp": activity.timestamp,
                    "metadata": {}  # Placeholder
                }
                for activity in activities
            ]
        except Exception as e:
            logger.error(f"Error getting activity feed: {e}")
            raise
    
    async def get_compliance_status(self, organization_id: int) -> Dict[str, Any]:
        """Get compliance status"""
        try:
            compliance = self.django_models['compliance_status'].objects.latest('updated_at')
            
            return {
                "compliance_percentage": compliance.compliance_percent,
                "audit_trail": compliance.audit_trail,
                "system_health": compliance.system_health,
                "last_audit": compliance.updated_at,
                "violations": [],  # Placeholder
                "recommendations": []  # Placeholder
            }
        except Exception as e:
            logger.error(f"Error getting compliance status: {e}")
            raise
    
    def _calculate_growth_rate(self, historical_data, metric_type: str) -> float:
        """Calculate growth rate for a metric"""
        try:
            relevant_data = [item for item in historical_data if item.metric_type == metric_type]
            if len(relevant_data) < 2:
                return 0.0
            
            latest = relevant_data[0].metric_value
            previous = relevant_data[-1].metric_value
            
            if previous == 0:
                return 0.0
            
            return ((latest - previous) / previous) * 100
        except Exception as e:
            logger.error(f"Error calculating growth rate: {e}")
            return 0.0
    
    def has_permission(self, user, permission_name: str) -> bool:
        """Check if user has specific permission"""
        try:
            if not user or not user.role:
                return False
            
            # Get user's role
            from django.apps import apps
            role_model = apps.get_model('deelflow', 'Role')
            role = role_model.objects.get(name=user.role)
            
            # Check if role has permission
            return role.permissions.filter(name=permission_name).exists()
        except Exception as e:
            logger.error(f"Error checking permission: {e}")
            return False
