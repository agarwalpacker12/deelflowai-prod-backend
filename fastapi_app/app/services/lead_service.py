"""
Lead service for handling lead-related business logic
"""

from typing import List, Optional
from app.schemas.lead import LeadCreate, LeadUpdate
from app.core.exceptions import NotFoundError, ValidationError
import os
import sys
import django

# Add the Django project root to the Python path
django_project_root = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'deelflowai-backend')
sys.path.append(django_project_root)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deelflow.settings')
django.setup()

from deelflow.models import Lead as DjangoLead

class LeadService:
    """Service for handling lead operations"""
    
    def has_permission(self, user, permission_name: str) -> bool:
        """Check if user has permission"""
        # For now, return True for all permissions (mock implementation)
        return True
    
    async def get_leads(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        lead_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[DjangoLead]:
        """Get list of leads with filtering and pagination"""
        queryset = DjangoLead.objects.all()
        
        # Apply filters
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) |
                models.Q(email__icontains=search) |
                models.Q(phone__icontains=search)
            )
        
        if lead_type:
            queryset = queryset.filter(lead_type=lead_type)
        
        if status:
            queryset = queryset.filter(status=status)
        
        # Apply pagination
        return list(queryset[skip:skip + limit])
    
    async def get_lead_by_id(self, lead_id: int) -> Optional[DjangoLead]:
        """Get lead by ID"""
        try:
            return DjangoLead.objects.get(id=lead_id)
        except DjangoLead.DoesNotExist:
            return None
    
    async def create_lead(self, lead_data: LeadCreate) -> DjangoLead:
        """Create a new lead"""
        try:
            # Convert LeadCreate to Django model fields
            lead_dict = lead_data.dict()
            
            # Create the lead
            lead = DjangoLead.objects.create(
                name=lead_dict.get('name', 'Unknown Lead'),
                email=lead_dict.get('email'),
                phone=lead_dict.get('phone'),
                address=lead_dict.get('address', ''),
                city=lead_dict.get('city', ''),
                state=lead_dict.get('state', ''),
                zipcode=lead_dict.get('zipcode', ''),
                source=lead_dict.get('source', 'website'),
                motivation_score=lead_dict.get('motivation_score', 0.5),
                property_condition=lead_dict.get('property_condition', 'unknown'),
                financial_situation=lead_dict.get('financial_situation', 'unknown'),
                timeline_urgency=lead_dict.get('timeline_urgency', 'medium'),
                negotiation_style=lead_dict.get('negotiation_style', 'flexible'),
                notes=lead_dict.get('notes', ''),
                status=lead_dict.get('status', 'new'),
                responded=lead_dict.get('responded', False)
            )
            
            return lead
            
        except Exception as e:
            raise ValidationError(f"Failed to create lead: {str(e)}")
    
    async def update_lead(self, lead_id: int, lead_data: LeadUpdate) -> DjangoLead:
        """Update lead information"""
        try:
            lead = await self.get_lead_by_id(lead_id)
            if not lead:
                raise NotFoundError("Lead not found")
            
            # Update fields
            update_dict = lead_data.dict(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(lead, field, value)
            
            lead.save()
            return lead
            
        except Exception as e:
            raise ValidationError(f"Failed to update lead: {str(e)}")
    
    async def delete_lead(self, lead_id: int) -> bool:
        """Delete lead"""
        try:
            lead = await self.get_lead_by_id(lead_id)
            if not lead:
                raise NotFoundError("Lead not found")
            
            lead.delete()
            return True
            
        except Exception as e:
            raise ValidationError(f"Failed to delete lead: {str(e)}")