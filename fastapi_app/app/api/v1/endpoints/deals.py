"""
Deal management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.core.security import get_current_user, require_permission
from app.core.exceptions import NotFoundError, AuthorizationError
from app.services.deal_service import DealService
from app.schemas.deal import DealResponse, DealCreate, DealUpdate
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=List[DealResponse])
async def get_deals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    status: Optional[str] = None,
    deal_type: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """Get list of deals with filtering and pagination"""
    try:
        deal_service = DealService()
        
        # Check permissions
        if not deal_service.has_permission(current_user, "view_deal"):
            raise AuthorizationError("Permission to view deals required")
        
        deals = await deal_service.get_deals(
            skip=skip,
            limit=limit,
            search=search,
            status=status,
            deal_type=deal_type
        )
        
        return [DealResponse.from_orm(deal) for deal in deals]
    
    except Exception as e:
        logger.error(f"Get deals error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve deals"
        )

@router.get("/{deal_id}", response_model=DealResponse)
async def get_deal(
    deal_id: int,
    current_user = Depends(get_current_user)
):
    """Get deal by ID"""
    try:
        deal_service = DealService()
        
        # Check permissions
        if not deal_service.has_permission(current_user, "view_deal"):
            raise AuthorizationError("Permission to view deals required")
        
        deal = await deal_service.get_deal_by_id(deal_id)
        if not deal:
            raise NotFoundError("Deal not found")
        
        return DealResponse.from_orm(deal)
    
    except Exception as e:
        logger.error(f"Get deal error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve deal"
        )

@router.post("/", response_model=DealResponse)
async def create_deal(
    deal_data: DealCreate,
    current_user = Depends(require_permission("add_deal"))
):
    """Create a new deal"""
    try:
        deal_service = DealService()
        
        deal = await deal_service.create_deal(deal_data)
        return DealResponse.from_orm(deal)
    
    except Exception as e:
        logger.error(f"Create deal error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create deal"
        )

@router.put("/{deal_id}", response_model=DealResponse)
async def update_deal(
    deal_id: int,
    deal_data: DealUpdate,
    current_user = Depends(require_permission("change_deal"))
):
    """Update deal information"""
    try:
        deal_service = DealService()
        
        deal = await deal_service.get_deal_by_id(deal_id)
        if not deal:
            raise NotFoundError("Deal not found")
        
        updated_deal = await deal_service.update_deal(deal_id, deal_data)
        return DealResponse.from_orm(updated_deal)
    
    except Exception as e:
        logger.error(f"Update deal error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update deal"
        )

@router.delete("/{deal_id}")
async def delete_deal(
    deal_id: int,
    current_user = Depends(require_permission("delete_deal"))
):
    """Delete deal"""
    try:
        deal_service = DealService()
        
        deal = await deal_service.get_deal_by_id(deal_id)
        if not deal:
            raise NotFoundError("Deal not found")
        
        await deal_service.delete_deal(deal_id)
        return {"message": "Deal deleted successfully"}
    
    except Exception as e:
        logger.error(f"Delete deal error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete deal"
        )

@router.post("/{deal_id}/close")
async def close_deal(
    deal_id: int,
    current_user = Depends(require_permission("change_deal"))
):
    """Close a deal"""
    try:
        deal_service = DealService()
        
        deal = await deal_service.get_deal_by_id(deal_id)
        if not deal:
            raise NotFoundError("Deal not found")
        
        await deal_service.close_deal(deal_id)
        return {"message": "Deal closed successfully"}
    
    except Exception as e:
        logger.error(f"Close deal error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to close deal"
        )

@router.get("/{deal_id}/milestones")
async def get_deal_milestones(
    deal_id: int,
    current_user = Depends(get_current_user)
):
    """Get deal milestones"""
    try:
        deal_service = DealService()
        
        # Check permissions
        if not deal_service.has_permission(current_user, "view_deal"):
            raise AuthorizationError("Permission to view deals required")
        
        deal = await deal_service.get_deal_by_id(deal_id)
        if not deal:
            raise NotFoundError("Deal not found")
        
        milestones = await deal_service.get_deal_milestones(deal_id)
        return milestones
    
    except Exception as e:
        logger.error(f"Get deal milestones error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve deal milestones"
        )
