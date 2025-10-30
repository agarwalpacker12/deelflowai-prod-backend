"""
Property management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.core.auth_middleware import get_current_user, require_permission
from app.core.exceptions import NotFoundError, AuthorizationError
from app.services.property_service import PropertyService
from app.schemas.property import PropertyResponse, PropertyCreate, PropertyUpdate
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=List[PropertyResponse])
async def get_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    current_user = Depends(get_current_user)
):
    """Get list of properties with filtering and pagination"""
    try:
        property_service = PropertyService()
        
        # Check permissions
        if not property_service.has_permission(current_user, "view_property"):
            raise AuthorizationError("Permission to view properties required")
        
        properties = await property_service.get_properties(
            skip=skip,
            limit=limit,
            search=search,
            property_type=property_type,
            min_price=min_price,
            max_price=max_price
        )
        
        return [PropertyResponse.from_orm(property) for property in properties]
    
    except Exception as e:
        logger.error(f"Get properties error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve properties"
        )

@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(
    property_id: int,
    current_user = Depends(get_current_user)
):
    """Get property by ID"""
    try:
        property_service = PropertyService()
        
        # Check permissions
        if not property_service.has_permission(current_user, "view_property"):
            raise AuthorizationError("Permission to view properties required")
        
        property = await property_service.get_property_by_id(property_id)
        if not property:
            raise NotFoundError("Property not found")
        
        return PropertyResponse.from_orm(property)
    
    except Exception as e:
        logger.error(f"Get property error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve property"
        )

@router.post("/", response_model=PropertyResponse)
async def create_property(
    property_data: PropertyCreate,
    current_user = Depends(require_permission("add_property"))
):
    """Create a new property"""
    try:
        property_service = PropertyService()
        
        property = await property_service.create_property(property_data)
        return PropertyResponse.from_orm(property)
    
    except Exception as e:
        logger.error(f"Create property error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create property"
        )

@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: int,
    property_data: PropertyUpdate,
    current_user = Depends(require_permission("change_property"))
):
    """Update property information"""
    try:
        property_service = PropertyService()
        
        property = await property_service.get_property_by_id(property_id)
        if not property:
            raise NotFoundError("Property not found")
        
        updated_property = await property_service.update_property(property_id, property_data)
        return PropertyResponse.from_orm(updated_property)
    
    except Exception as e:
        logger.error(f"Update property error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update property"
        )

@router.delete("/{property_id}")
async def delete_property(
    property_id: int,
    current_user = Depends(require_permission("delete_property"))
):
    """Delete property"""
    try:
        property_service = PropertyService()
        
        property = await property_service.get_property_by_id(property_id)
        if not property:
            raise NotFoundError("Property not found")
        
        await property_service.delete_property(property_id)
        return {"message": "Property deleted successfully"}
    
    except Exception as e:
        logger.error(f"Delete property error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete property"
        )

@router.get("/{property_id}/ai-analysis")
async def get_property_ai_analysis(
    property_id: int,
    current_user = Depends(get_current_user)
):
    """Get AI analysis for a property"""
    try:
        property_service = PropertyService()
        
        # Check permissions
        if not property_service.has_permission(current_user, "view_property"):
            raise AuthorizationError("Permission to view properties required")
        
        property = await property_service.get_property_by_id(property_id)
        if not property:
            raise NotFoundError("Property not found")
        
        analysis = await property_service.get_property_ai_analysis(property_id)
        return analysis
    
    except Exception as e:
        logger.error(f"Get property AI analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve property AI analysis"
        )
