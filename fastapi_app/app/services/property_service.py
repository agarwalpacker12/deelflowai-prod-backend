"""
Property service for business logic
"""

from typing import List, Optional, Dict, Any
from decimal import Decimal
from app.schemas.property import PropertyCreate, PropertyUpdate
from app.core.exceptions import NotFoundError, ValidationError
import logging

logger = logging.getLogger(__name__)

class PropertyService:
    """Property service class"""
    
    def __init__(self):
        self.django_property_model = None
        self.django_property_ai_model = None
        self._setup_django_models()
    
    def _setup_django_models(self):
        """Setup Django models"""
        try:
            import django
            from django.apps import apps
            
            self.django_property_model = apps.get_model('deelflow', 'Property')
            self.django_property_ai_model = apps.get_model('deelflow', 'PropertyAIAnalysis')
        except Exception as e:
            logger.error(f"Failed to setup Django models: {e}")
    
    async def get_property_by_id(self, property_id: int):
        """Get property by ID"""
        try:
            return self.django_property_model.objects.get(id=property_id)
        except self.django_property_model.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error getting property by ID: {e}")
            raise
    
    async def get_properties(self, skip: int = 0, limit: int = 100, search: str = None,
                            property_type: str = None, min_price: float = None, max_price: float = None):
        """Get properties with filtering and pagination"""
        try:
            queryset = self.django_property_model.objects.all()
            
            # Apply filters
            if search:
                queryset = queryset.filter(
                    models.Q(address__icontains=search) |
                    models.Q(city__icontains=search) |
                    models.Q(state__icontains=search)
                )
            
            if property_type:
                queryset = queryset.filter(property_type=property_type)
            
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
            
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
            
            # Apply pagination
            return queryset[skip:skip + limit]
        except Exception as e:
            logger.error(f"Error getting properties: {e}")
            raise
    
    async def create_property(self, property_data: PropertyCreate):
        """Create a new property"""
        try:
            # Create property
            property = self.django_property_model.objects.create(
                address=property_data.address,
                city=property_data.city,
                state=property_data.state,
                zipcode=property_data.zipcode,
                property_type=property_data.property_type,
                price=property_data.price,
                bedrooms=property_data.bedrooms,
                bathrooms=property_data.bathrooms,
                square_feet=property_data.square_feet,
                lot_size=property_data.lot_size,
                year_built=property_data.year_built,
                description=property_data.description,
                images=property_data.images
            )
            
            return property
        except Exception as e:
            logger.error(f"Error creating property: {e}")
            raise
    
    async def update_property(self, property_id: int, property_data: PropertyUpdate):
        """Update property information"""
        try:
            property = await self.get_property_by_id(property_id)
            if not property:
                raise NotFoundError("Property not found")
            
            # Update fields
            update_data = property_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(property, field, value)
            
            property.save()
            return property
        except Exception as e:
            logger.error(f"Error updating property: {e}")
            raise
    
    async def delete_property(self, property_id: int):
        """Delete property"""
        try:
            property = await self.get_property_by_id(property_id)
            if not property:
                raise NotFoundError("Property not found")
            
            property.delete()
        except Exception as e:
            logger.error(f"Error deleting property: {e}")
            raise
    
    async def get_property_ai_analysis(self, property_id: int):
        """Get AI analysis for a property"""
        try:
            property = await self.get_property_by_id(property_id)
            if not property:
                raise NotFoundError("Property not found")
            
            # Get AI analysis
            analysis = self.django_property_ai_model.objects.filter(
                address=property.address
            ).first()
            
            if not analysis:
                return None
            
            return {
                "ai_confidence": analysis.ai_confidence,
                "distress_level": analysis.distress_level,
                "motivation": analysis.motivation,
                "timeline": analysis.timeline,
                "roi_percent": analysis.roi_percent,
                "cap_rate": analysis.cap_rate,
                "cash_flow": analysis.cash_flow,
                "market_stability_score": analysis.market_stability_score,
                "comparables_confidence": analysis.comparables_confidence,
                "analysis_date": analysis.updated_at
            }
        except Exception as e:
            logger.error(f"Error getting property AI analysis: {e}")
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
