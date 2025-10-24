"""
Campaign service for business logic
"""

from typing import List, Optional, Dict, Any
from decimal import Decimal
from app.schemas.campaign import CampaignCreate, CampaignUpdate
from app.core.exceptions import NotFoundError, ValidationError
import logging

logger = logging.getLogger(__name__)

class CampaignService:
    """Campaign service class"""
    
    def __init__(self):
        self.django_campaign_model = None
        self.django_lead_model = None
        self.django_user_model = None
        self._setup_django_models()
    
    def _setup_django_models(self):
        """Setup Django models"""
        try:
            import django
            from django.apps import apps
            
            self.django_campaign_model = apps.get_model('deelflow', 'Campaign')
            self.django_lead_model = apps.get_model('deelflow', 'Lead')
            self.django_user_model = apps.get_model('deelflow', 'User')
        except Exception as e:
            logger.error(f"Failed to setup Django models: {e}")
    
    async def get_campaign_by_id(self, campaign_id: int):
        """Get campaign by ID"""
        try:
            return self.django_campaign_model.objects.get(id=campaign_id)
        except self.django_campaign_model.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error getting campaign by ID: {e}")
            raise
    
    async def get_campaigns(self, skip: int = 0, limit: int = 100, search: str = None,
                           status: str = None, channel: str = None, organization_id: int = None):
        """Get campaigns with filtering and pagination"""
        try:
            queryset = self.django_campaign_model.objects.all()
            
            # Apply filters
            if search:
                queryset = queryset.filter(name__icontains=search)
            
            if status:
                queryset = queryset.filter(status=status)
            
            if channel:
                queryset = queryset.filter(channel=channel)
            
            if organization_id:
                # Filter by organization through users
                queryset = queryset.filter(created_by__organization_id=organization_id)
            
            # Apply pagination
            return queryset[skip:skip + limit]
        except Exception as e:
            logger.error(f"Error getting campaigns: {e}")
            raise
    
    async def create_campaign(self, campaign_data: CampaignCreate, organization_id: int):
        """Create a new campaign"""
        try:
            # Create campaign
            campaign = self.django_campaign_model.objects.create(
                name=campaign_data.name,
                campaign_type=campaign_data.campaign_type,
                channel=campaign_data.channel,
                budget=campaign_data.budget,
                scheduled_at=campaign_data.scheduled_at,
                geographic_scope_type=campaign_data.geographic_scope_type,
                geographic_scope_values=campaign_data.geographic_scope_values,
                location=campaign_data.location,
                property_type=campaign_data.property_type,
                minimum_equity=campaign_data.minimum_equity,
                min_price=campaign_data.min_price,
                max_price=campaign_data.max_price,
                distress_indicators=campaign_data.distress_indicators,
                subject_line=campaign_data.subject_line,
                email_content=campaign_data.email_content,
                use_ai_personalization=campaign_data.use_ai_personalization
            )
            
            return campaign
        except Exception as e:
            logger.error(f"Error creating campaign: {e}")
            raise
    
    async def update_campaign(self, campaign_id: int, campaign_data: CampaignUpdate):
        """Update campaign information"""
        try:
            campaign = await self.get_campaign_by_id(campaign_id)
            if not campaign:
                raise NotFoundError("Campaign not found")
            
            # Update fields
            update_data = campaign_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(campaign, field, value)
            
            campaign.save()
            return campaign
        except Exception as e:
            logger.error(f"Error updating campaign: {e}")
            raise
    
    async def delete_campaign(self, campaign_id: int):
        """Delete campaign"""
        try:
            campaign = await self.get_campaign_by_id(campaign_id)
            if not campaign:
                raise NotFoundError("Campaign not found")
            
            campaign.delete()
        except Exception as e:
            logger.error(f"Error deleting campaign: {e}")
            raise
    
    async def start_campaign(self, campaign_id: int):
        """Start a campaign"""
        try:
            campaign = await self.get_campaign_by_id(campaign_id)
            if not campaign:
                raise NotFoundError("Campaign not found")
            
            campaign.status = "active"
            campaign.save()
        except Exception as e:
            logger.error(f"Error starting campaign: {e}")
            raise
    
    async def pause_campaign(self, campaign_id: int):
        """Pause a campaign"""
        try:
            campaign = await self.get_campaign_by_id(campaign_id)
            if not campaign:
                raise NotFoundError("Campaign not found")
            
            campaign.status = "paused"
            campaign.save()
        except Exception as e:
            logger.error(f"Error pausing campaign: {e}")
            raise
    
    async def get_campaign_leads(self, campaign_id: int, skip: int = 0, limit: int = 100):
        """Get leads for a specific campaign"""
        try:
            campaign = await self.get_campaign_by_id(campaign_id)
            if not campaign:
                raise NotFoundError("Campaign not found")
            
            leads = self.django_lead_model.objects.filter(
                campaign_id=campaign_id
            )[skip:skip + limit]
            
            return leads
        except Exception as e:
            logger.error(f"Error getting campaign leads: {e}")
            raise
    
    async def get_campaign_performance(self, campaign_id: int) -> Dict[str, Any]:
        """Get campaign performance metrics"""
        try:
            campaign = await self.get_campaign_by_id(campaign_id)
            if not campaign:
                raise NotFoundError("Campaign not found")
            
            # Get campaign leads
            leads = self.django_lead_model.objects.filter(campaign_id=campaign_id)
            
            # Calculate metrics
            total_leads = leads.count()
            qualified_leads = leads.filter(status="qualified").count()
            converted_leads = leads.filter(status="converted").count()
            
            # Calculate rates
            qualification_rate = (qualified_leads / total_leads * 100) if total_leads > 0 else 0
            conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
            
            return {
                "campaign_id": campaign_id,
                "total_leads": total_leads,
                "qualified_leads": qualified_leads,
                "converted_leads": converted_leads,
                "qualification_rate": qualification_rate,
                "conversion_rate": conversion_rate,
                "status": campaign.status
            }
        except Exception as e:
            logger.error(f"Error getting campaign performance: {e}")
            raise
    
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
