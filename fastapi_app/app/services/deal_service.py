"""
Deal service for business logic
"""

from typing import List, Optional, Dict, Any
from decimal import Decimal
from app.schemas.deal import DealCreate, DealUpdate
from app.core.exceptions import NotFoundError, ValidationError
import logging

logger = logging.getLogger(__name__)

class DealService:
    """Deal service class"""
    
    def __init__(self):
        self.django_deal_model = None
        self.django_deal_milestone_model = None
        self._setup_django_models()
    
    def _setup_django_models(self):
        """Setup Django models"""
        try:
            import django
            from django.apps import apps
            
            self.django_deal_model = apps.get_model('deelflow', 'Deal')
            self.django_deal_milestone_model = apps.get_model('deelflow', 'DealMilestone')
        except Exception as e:
            logger.error(f"Failed to setup Django models: {e}")
    
    async def get_deal_by_id(self, deal_id: int):
        """Get deal by ID"""
        try:
            return self.django_deal_model.objects.get(id=deal_id)
        except self.django_deal_model.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error getting deal by ID: {e}")
            raise
    
    async def get_deals(self, skip: int = 0, limit: int = 100, search: str = None,
                       status: str = None, deal_type: str = None):
        """Get deals with filtering and pagination"""
        try:
            queryset = self.django_deal_model.objects.all()
            
            # Apply filters
            if search:
                queryset = queryset.filter(
                    models.Q(notes__icontains=search) |
                    models.Q(deal_type__icontains=search)
                )
            
            if status:
                queryset = queryset.filter(status=status)
            
            if deal_type:
                queryset = queryset.filter(deal_type=deal_type)
            
            # Apply pagination
            return queryset[skip:skip + limit]
        except Exception as e:
            logger.error(f"Error getting deals: {e}")
            raise
    
    async def create_deal(self, deal_data: DealCreate):
        """Create a new deal"""
        try:
            # Create deal
            deal = self.django_deal_model.objects.create(
                property_id=deal_data.property_id,
                buyer_lead_id=deal_data.buyer_lead_id,
                seller_lead_id=deal_data.seller_lead_id,
                deal_type=deal_data.deal_type,
                status=deal_data.status,
                offer_price=deal_data.offer_price,
                final_price=deal_data.final_price,
                commission=deal_data.commission,
                closing_date=deal_data.closing_date,
                notes=deal_data.notes
            )
            
            return deal
        except Exception as e:
            logger.error(f"Error creating deal: {e}")
            raise
    
    async def update_deal(self, deal_id: int, deal_data: DealUpdate):
        """Update deal information"""
        try:
            deal = await self.get_deal_by_id(deal_id)
            if not deal:
                raise NotFoundError("Deal not found")
            
            # Update fields
            update_data = deal_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(deal, field, value)
            
            deal.save()
            return deal
        except Exception as e:
            logger.error(f"Error updating deal: {e}")
            raise
    
    async def delete_deal(self, deal_id: int):
        """Delete deal"""
        try:
            deal = await self.get_deal_by_id(deal_id)
            if not deal:
                raise NotFoundError("Deal not found")
            
            deal.delete()
        except Exception as e:
            logger.error(f"Error deleting deal: {e}")
            raise
    
    async def close_deal(self, deal_id: int):
        """Close a deal"""
        try:
            deal = await self.get_deal_by_id(deal_id)
            if not deal:
                raise NotFoundError("Deal not found")
            
            deal.status = "closed"
            deal.save()
        except Exception as e:
            logger.error(f"Error closing deal: {e}")
            raise
    
    async def get_deal_milestones(self, deal_id: int):
        """Get deal milestones"""
        try:
            deal = await self.get_deal_by_id(deal_id)
            if not deal:
                raise NotFoundError("Deal not found")
            
            milestones = self.django_deal_milestone_model.objects.filter(
                deal_id=deal_id
            )
            
            return milestones
        except Exception as e:
            logger.error(f"Error getting deal milestones: {e}")
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
