"""
Lead management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.core.security import get_current_user, require_permission
from app.core.exceptions import NotFoundError, AuthorizationError
from app.services.lead_service import LeadService
from app.schemas.lead import LeadResponse, LeadCreate, LeadUpdate, DiscoveredLeadResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=List[LeadResponse])
async def get_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    status: Optional[str] = None,
    source: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """Get list of leads with filtering and pagination"""
    try:
        lead_service = LeadService()
        
        # Check permissions
        if not lead_service.has_permission(current_user, "view_lead"):
            raise AuthorizationError("Permission to view leads required")
        
        leads = await lead_service.get_leads(
            skip=skip,
            limit=limit,
            search=search,
            status=status,
            source=source
        )
        
        return [LeadResponse.from_orm(lead) for lead in leads]
    
    except Exception as e:
        logger.error(f"Get leads error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve leads"
        )

@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: int,
    current_user = Depends(get_current_user)
):
    """Get lead by ID"""
    try:
        lead_service = LeadService()
        
        # Check permissions
        if not lead_service.has_permission(current_user, "view_lead"):
            raise AuthorizationError("Permission to view leads required")
        
        lead = await lead_service.get_lead_by_id(lead_id)
        if not lead:
            raise NotFoundError("Lead not found")
        
        return LeadResponse.from_orm(lead)
    
    except Exception as e:
        logger.error(f"Get lead error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve lead"
        )

@router.post("/", response_model=LeadResponse)
async def create_lead(
    lead_data: LeadCreate,
    current_user = Depends(require_permission("add_lead"))
):
    """Create a new lead"""
    try:
        lead_service = LeadService()
        
        lead = await lead_service.create_lead(lead_data)
        return LeadResponse.from_orm(lead)
    
    except Exception as e:
        logger.error(f"Create lead error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create lead"
        )

@router.put("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: int,
    lead_data: LeadUpdate,
    current_user = Depends(require_permission("change_lead"))
):
    """Update lead information"""
    try:
        lead_service = LeadService()
        
        lead = await lead_service.get_lead_by_id(lead_id)
        if not lead:
            raise NotFoundError("Lead not found")
        
        updated_lead = await lead_service.update_lead(lead_id, lead_data)
        return LeadResponse.from_orm(updated_lead)
    
    except Exception as e:
        logger.error(f"Update lead error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update lead"
        )

@router.delete("/{lead_id}")
async def delete_lead(
    lead_id: int,
    current_user = Depends(require_permission("delete_lead"))
):
    """Delete lead"""
    try:
        lead_service = LeadService()
        
        lead = await lead_service.get_lead_by_id(lead_id)
        if not lead:
            raise NotFoundError("Lead not found")
        
        await lead_service.delete_lead(lead_id)
        return {"message": "Lead deleted successfully"}
    
    except Exception as e:
        logger.error(f"Delete lead error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete lead"
        )

@router.get("/discovered/", response_model=List[DiscoveredLeadResponse])
async def get_discovered_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    source: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """Get discovered leads from AI scraping"""
    try:
        lead_service = LeadService()
        
        # Check permissions
        if not lead_service.has_permission(current_user, "view_lead"):
            raise AuthorizationError("Permission to view leads required")
        
        leads = await lead_service.get_discovered_leads(
            skip=skip,
            limit=limit,
            source=source
        )
        
        return [DiscoveredLeadResponse.from_orm(lead) for lead in leads]
    
    except Exception as e:
        logger.error(f"Get discovered leads error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve discovered leads"
        )

@router.post("/{lead_id}/qualify")
async def qualify_lead(
    lead_id: int,
    current_user = Depends(require_permission("change_lead"))
):
    """Qualify a lead"""
    try:
        lead_service = LeadService()
        
        lead = await lead_service.get_lead_by_id(lead_id)
        if not lead:
            raise NotFoundError("Lead not found")
        
        await lead_service.qualify_lead(lead_id)
        return {"message": "Lead qualified successfully"}
    
    except Exception as e:
        logger.error(f"Qualify lead error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to qualify lead"
        )

@router.post("/{lead_id}/convert")
async def convert_lead(
    lead_id: int,
    current_user = Depends(require_permission("change_lead"))
):
    """Convert a lead"""
    try:
        lead_service = LeadService()
        
        lead = await lead_service.get_lead_by_id(lead_id)
        if not lead:
            raise NotFoundError("Lead not found")
        
        await lead_service.convert_lead(lead_id)
        return {"message": "Lead converted successfully"}
    
    except Exception as e:
        logger.error(f"Convert lead error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to convert lead"
        )
