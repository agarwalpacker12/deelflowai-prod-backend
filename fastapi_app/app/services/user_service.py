"""
User service for business logic
"""

from typing import List, Optional
from app.core.security import get_password_hash, verify_password
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import NotFoundError, ValidationError
from asgiref.sync import sync_to_async
import logging

logger = logging.getLogger(__name__)

class UserService:
    """User service class"""
    
    def __init__(self):
        self.django_user_model = None
        self.django_organization_model = None
        self.django_role_model = None
        self._setup_django_models()
    
    def _setup_django_models(self):
        """Setup Django models"""
        try:
            import django
            from django.apps import apps
            
            self.django_user_model = apps.get_model('deelflow', 'User')
            self.django_organization_model = apps.get_model('deelflow', 'Organization')
            self.django_role_model = apps.get_model('deelflow', 'Role')
        except Exception as e:
            logger.error(f"Failed to setup Django models: {e}")
    
    async def get_user_by_id(self, user_id: int):
        """Get user by ID"""
        try:
            return await sync_to_async(self.django_user_model.objects.get)(id=user_id)
        except self.django_user_model.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            raise
    
    async def get_user_by_email(self, email: str):
        """Get user by email"""
        try:
            return await sync_to_async(self.django_user_model.objects.get)(email=email)
        except self.django_user_model.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            raise
    
    async def authenticate_user(self, email: str, password: str):
        """Authenticate user with email and password"""
        try:
            user = await self.get_user_by_email(email)
            if user and verify_password(password, user.password):
                return user
            return None
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            raise
    
    async def create_user(self, user_data: UserCreate):
        """Create a new user"""
        try:
            # Hash password
            hashed_password = get_password_hash(user_data.password)
            
            # Get organization if provided
            organization = None
            if user_data.organization_id:
                organization = await sync_to_async(self.django_organization_model.objects.get)(id=user_data.organization_id)
            
            # Create user
            user = await sync_to_async(self.django_user_model.objects.create)(
                email=user_data.email,
                password=hashed_password,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                phone=user_data.phone,
                role=user_data.role,
                organization=organization,
                is_active=user_data.is_active,
                is_verified=user_data.is_verified
            )
            
            return user
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    async def update_user(self, user_id: int, user_data: UserUpdate):
        """Update user information"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise NotFoundError("User not found")
            
            # Update fields
            update_data = user_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(user, field, value)
            
            await sync_to_async(user.save)()
            return user
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            raise
    
    async def delete_user(self, user_id: int):
        """Delete user"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise NotFoundError("User not found")
            
            await sync_to_async(user.delete)()
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            raise
    
    async def get_users(self, skip: int = 0, limit: int = 100, search: str = None, 
                       role: str = None, organization_id: int = None):
        """Get users with filtering and pagination"""
        try:
            from django.db import models
            
            queryset = self.django_user_model.objects.all()
            
            # Apply filters
            if search:
                queryset = queryset.filter(
                    models.Q(first_name__icontains=search) |
                    models.Q(last_name__icontains=search) |
                    models.Q(email__icontains=search)
                )
            
            if role:
                queryset = queryset.filter(role=role)
            
            if organization_id:
                queryset = queryset.filter(organization_id=organization_id)
            
            # Apply pagination
            return await sync_to_async(list)(queryset[skip:skip + limit])
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            raise
    
    async def get_user_roles(self, user_id: int):
        """Get user roles and permissions"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise NotFoundError("User not found")
            
            # Get user's role
            if user.role:
                role = await sync_to_async(self.django_role_model.objects.get)(name=user.role)
                return [role]
            
            return []
        except Exception as e:
            logger.error(f"Error getting user roles: {e}")
            raise
    
    async def assign_role(self, user_id: int, role_id: int):
        """Assign role to user"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise NotFoundError("User not found")
            
            role = await sync_to_async(self.django_role_model.objects.get)(id=role_id)
            user.role = role.name
            await sync_to_async(user.save)()
        except Exception as e:
            logger.error(f"Error assigning role: {e}")
            raise
    
    async def remove_role(self, user_id: int, role_id: int):
        """Remove role from user"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise NotFoundError("User not found")
            
            user.role = "user"  # Default role
            await sync_to_async(user.save)()
        except Exception as e:
            logger.error(f"Error removing role: {e}")
            raise
    
    async def has_permission(self, user, permission_name: str) -> bool:
        """Check if user has specific permission"""
        try:
            if not user or not user.role:
                return False
            
            # Get user's role
            role = await sync_to_async(self.django_role_model.objects.get)(name=user.role)
            
            # Check if role has permission
            return await sync_to_async(role.permissions.filter(name=permission_name).exists)()
        except Exception as e:
            logger.error(f"Error checking permission: {e}")
            return False
