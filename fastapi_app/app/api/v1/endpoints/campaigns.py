"""
Campaign management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.core.auth_middleware import get_current_user, require_permission
from app.core.exceptions import NotFoundError, AuthorizationError
from app.services.campaign_service import CampaignService
from app.schemas.campaign import CampaignResponse, CampaignCreate, CampaignUpdate, CampaignListResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=CampaignListResponse)
async def get_campaigns(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    status: Optional[str] = None,
    channel: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """Get list of campaigns with filtering and pagination"""
    try:
        campaign_service = CampaignService()
        
        # Check permissions
        if not campaign_service.has_permission(current_user, "view_campaign"):
            raise AuthorizationError("Permission to view campaigns required")
        
        campaigns = await campaign_service.get_campaigns(
            skip=skip,
            limit=limit,
            search=search,
            status=status,
            channel=channel
        )
        
        total = len(campaigns)  # This should be improved with proper count query
        
        return CampaignListResponse(
            campaigns=[CampaignResponse.from_orm(campaign) for campaign in campaigns],
            total=total,
            page=skip // limit + 1,
            limit=limit,
            has_next=skip + limit < total,
            has_prev=skip > 0
        )
    
    except Exception as e:
        logger.error(f"Get campaigns error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve campaigns"
        )

@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: int,
    current_user = Depends(get_current_user)
):
    """Get specific campaign by ID"""
    try:
        campaign_service = CampaignService()
        
        # Check permissions
        if not campaign_service.has_permission(current_user, "view_campaign"):
            raise AuthorizationError("Permission to view campaigns required")
        
        campaign = await campaign_service.get_campaign_by_id(campaign_id)
        if not campaign:
            raise NotFoundError("Campaign not found")
        
        return CampaignResponse.from_orm(campaign)
    
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    except Exception as e:
        logger.error(f"Get campaign error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve campaign"
        )

@router.post("/", response_model=CampaignResponse)
async def create_campaign(
    campaign_data: CampaignCreate,
    current_user = Depends(require_permission("add_campaign"))
):
    """Create a new campaign"""
    try:
        campaign_service = CampaignService()
        
        campaign = await campaign_service.create_campaign(campaign_data)
        
        return CampaignResponse.from_orm(campaign)
    
    except Exception as e:
        logger.error(f"Create campaign error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create campaign"
        )

@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: int,
    campaign_data: CampaignUpdate,
    current_user = Depends(require_permission("change_campaign"))
):
    """Update an existing campaign"""
    try:
        campaign_service = CampaignService()
        
        campaign = await campaign_service.update_campaign(campaign_id, campaign_data)
        if not campaign:
            raise NotFoundError("Campaign not found")
        
        return CampaignResponse.from_orm(campaign)
    
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    except Exception as e:
        logger.error(f"Update campaign error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update campaign"
        )

@router.delete("/{campaign_id}")
async def delete_campaign(
    campaign_id: int,
    current_user = Depends(require_permission("delete_campaign"))
):
    """Delete a campaign"""
    try:
        campaign_service = CampaignService()
        
        success = await campaign_service.delete_campaign(campaign_id)
        if not success:
            raise NotFoundError("Campaign not found")
        
        return {"message": "Campaign deleted successfully"}
    
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    except Exception as e:
        logger.error(f"Delete campaign error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete campaign"
        )

@router.post("/{campaign_id}/start")
async def start_campaign(
    campaign_id: int,
    current_user = Depends(require_permission("change_campaign"))
):
    """Start a campaign"""
    try:
        campaign_service = CampaignService()
        
        success = await campaign_service.start_campaign(campaign_id)
        if not success:
            raise NotFoundError("Campaign not found")
        
        return {"message": "Campaign started successfully"}
    
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    except Exception as e:
        logger.error(f"Start campaign error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start campaign"
        )

@router.post("/{campaign_id}/pause")
async def pause_campaign(
    campaign_id: int,
    current_user = Depends(require_permission("change_campaign"))
):
    """Pause a campaign"""
    try:
        campaign_service = CampaignService()
        
        success = await campaign_service.pause_campaign(campaign_id)
        if not success:
            raise NotFoundError("Campaign not found")
        
        return {"message": "Campaign paused successfully"}
    
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    except Exception as e:
        logger.error(f"Pause campaign error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to pause campaign"
        )

@router.get("/{campaign_id}/performance")
async def get_campaign_performance(
    campaign_id: int,
    current_user = Depends(get_current_user)
):
    """Get campaign performance metrics"""
    try:
        campaign_service = CampaignService()
        
        # Check permissions
        if not campaign_service.has_permission(current_user, "view_campaign"):
            raise AuthorizationError("Permission to view campaigns required")
        
        performance = await campaign_service.get_campaign_performance(campaign_id)
        
        return performance
    
    except Exception as e:
        logger.error(f"Get campaign performance error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve campaign performance"
        )
