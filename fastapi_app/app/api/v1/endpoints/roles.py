"""
Enhanced Role and permission management endpoints
Handles complex permission structure with enabled booleans
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
from app.core.auth_middleware import get_current_user, require_permission
from app.core.exceptions import NotFoundError, AuthorizationError
from app.services.role_service import RoleService
from app.schemas.role import RoleResponse, RoleCreate, RoleUpdate, RoleListResponse, PermissionResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=Dict[str, Any])
async def get_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None
):
    """Get list of roles with filtering and pagination"""
    try:
        role_service = RoleService()
        
        roles = role_service.get_roles(
            skip=skip,
            limit=limit,
            search=search
        )
        
        total = len(roles)  # This should be improved with proper count query
        
        return {
            "status": "success",
            "data": [
                {
                    "id": role.id,
                    "name": role.name,
                    "label": role.label,
                    "permissions": [
                        {
                            "id": perm.id,
                            "name": perm.name,
                            "label": perm.label
                        } for perm in role.permissions.all()
                    ],
                    "created_at": role.created_at,
                    "updated_at": role.updated_at
                } for role in roles
            ],
            "total": total,
            "page": skip // limit + 1,
            "limit": limit,
            "has_next": skip + limit < total,
            "has_prev": skip > 0
        }
    
    except Exception as e:
        logger.error(f"Get roles error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve roles"
        )

@router.get("/{role_id}/", response_model=Dict[str, Any])
async def get_role(role_id: int):
    """Get role by ID"""
    try:
        role_service = RoleService()
        
        role = role_service.get_role_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        return {
            "status": "success",
            "data": {
                "id": role.id,
                "name": role.name,
                "label": role.label,
                "permissions": [
                    {
                        "id": perm.id,
                        "name": perm.name,
                        "label": perm.label
                    } for perm in role.permissions.all()
                ],
                "created_at": role.created_at,
                "updated_at": role.updated_at
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get role error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve role"
        )

@router.post("/", response_model=Dict[str, Any])
async def create_role(role_data: Dict[str, Any]):
    """Create a new role with complex permission structure support"""
    try:
        role_service = RoleService()
        
        result = role_service.create_role(role_data)
        
        if result["status"] == "error":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create role error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create role"
        )

@router.put("/{role_id}/", response_model=Dict[str, Any])
async def update_role(role_id: int, role_data: Dict[str, Any]):
    """Update an existing role with complex permission structure support"""
    try:
        role_service = RoleService()
        
        result = role_service.update_role(role_id, role_data)
        
        if result["status"] == "error":
            if "not found" in result["message"].lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=result["message"]
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result["message"]
                )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update role error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update role"
        )

@router.delete("/{role_id}/", response_model=Dict[str, Any])
async def delete_role(role_id: int):
    """Delete a role"""
    try:
        role_service = RoleService()
        
        result = role_service.delete_role(role_id)
        
        if result["status"] == "error":
            if "not found" in result["message"].lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=result["message"]
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result["message"]
                )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete role error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete role"
        )

@router.get("/permissions/", response_model=Dict[str, Any])
async def get_permissions():
    """Get all available permissions"""
    try:
        role_service = RoleService()
        
        result = role_service.get_permissions()
        
        if result["status"] == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["message"]
            )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get permissions error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve permissions"
        )
