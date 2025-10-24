"""
User management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.core.security import get_current_user, require_permission
from app.core.exceptions import NotFoundError, AuthorizationError
from app.services.user_service import UserService
from app.schemas.user import UserResponse, UserCreate, UserUpdate, UserListResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=UserListResponse)
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    role: Optional[str] = None,
    organization_id: Optional[int] = None,
    current_user = Depends(get_current_user)
):
    """Get list of users with filtering and pagination"""
    try:
        user_service = UserService()
        
        # Check permissions
        if not user_service.has_permission(current_user, "view_user"):
            raise AuthorizationError("Permission to view users required")
        
        users = await user_service.get_users(
            skip=skip,
            limit=limit,
            search=search,
            role=role,
            organization_id=organization_id
        )
        
        total = len(users)  # This should be improved with proper count query
        
        return UserListResponse(
            users=[UserResponse.from_orm(user) for user in users],
            total=total,
            page=skip // limit + 1,
            limit=limit,
            has_next=skip + limit < total,
            has_prev=skip > 0
        )
    
    except Exception as e:
        logger.error(f"Get users error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user = Depends(get_current_user)
):
    """Get specific user by ID"""
    try:
        user_service = UserService()
        
        # Check permissions
        if not user_service.has_permission(current_user, "view_user"):
            raise AuthorizationError("Permission to view users required")
        
        user = await user_service.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        
        return UserResponse.from_orm(user)
    
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except Exception as e:
        logger.error(f"Get user error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user"
        )

@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    current_user = Depends(require_permission("add_user"))
):
    """Create a new user"""
    try:
        user_service = UserService()
        
        user = await user_service.create_user(user_data)
        
        return UserResponse.from_orm(user)
    
    except Exception as e:
        logger.error(f"Create user error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create user"
        )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user = Depends(require_permission("change_user"))
):
    """Update an existing user"""
    try:
        user_service = UserService()
        
        user = await user_service.update_user(user_id, user_data)
        if not user:
            raise NotFoundError("User not found")
        
        return UserResponse.from_orm(user)
    
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except Exception as e:
        logger.error(f"Update user error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update user"
        )

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user = Depends(require_permission("delete_user"))
):
    """Delete a user"""
    try:
        user_service = UserService()
        
        success = await user_service.delete_user(user_id)
        if not success:
            raise NotFoundError("User not found")
        
        return {"message": "User deleted successfully"}
    
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except Exception as e:
        logger.error(f"Delete user error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )

@router.get("/{user_id}/roles", response_model=List[str])
async def get_user_roles(
    user_id: int,
    current_user = Depends(get_current_user)
):
    """Get roles for a specific user"""
    try:
        user_service = UserService()
        
        # Check permissions
        if not user_service.has_permission(current_user, "view_user"):
            raise AuthorizationError("Permission to view users required")
        
        roles = await user_service.get_user_roles(user_id)
        
        return roles
    
    except Exception as e:
        logger.error(f"Get user roles error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user roles"
        )

@router.post("/{user_id}/assign-role")
async def assign_role(
    user_id: int,
    role_id: int,
    current_user = Depends(require_permission("change_user"))
):
    """Assign a role to a user"""
    try:
        user_service = UserService()
        
        success = await user_service.assign_role(user_id, role_id)
        if not success:
            raise NotFoundError("User or role not found")
        
        return {"message": "Role assigned successfully"}
    
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or role not found"
        )
    except Exception as e:
        logger.error(f"Assign role error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to assign role"
        )

@router.delete("/{user_id}/remove-role")
async def remove_role(
    user_id: int,
    role_id: int,
    current_user = Depends(require_permission("change_user"))
):
    """Remove a role from a user"""
    try:
        user_service = UserService()
        
        success = await user_service.remove_role(user_id, role_id)
        if not success:
            raise NotFoundError("User or role not found")
        
        return {"message": "Role removed successfully"}
    
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or role not found"
        )
    except Exception as e:
        logger.error(f"Remove role error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to remove role"
        )
