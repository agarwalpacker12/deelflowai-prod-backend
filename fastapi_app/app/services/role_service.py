"""
Enhanced Role and permission service for business logic
Handles complex permission structure with enabled booleans
"""

from typing import List, Optional, Dict, Any
from app.schemas.role import RoleCreate, RoleUpdate, PermissionGroup, PermissionWithEnabled
from app.core.exceptions import NotFoundError, ValidationError
import logging

logger = logging.getLogger(__name__)

class RoleService:
    """Enhanced role service class"""
    
    def __init__(self):
        self.django_role_model = None
        self.django_permission_model = None
        self._setup_django_models()
    
    def _setup_django_models(self):
        """Setup Django models"""
        try:
            import django
            from django.apps import apps
            
            self.django_role_model = apps.get_model('deelflow', 'Role')
            self.django_permission_model = apps.get_model('deelflow', 'Permission')
        except Exception as e:
            logger.error(f"Failed to setup Django models: {e}")
    
    def _extract_permission_ids(self, role_data: Dict[str, Any]) -> List[int]:
        """Extract permission IDs from complex frontend structure"""
        permission_ids = []
        
        if 'permissions' in role_data and role_data['permissions']:
            for group in role_data['permissions']:
                if isinstance(group, dict) and 'permissions' in group:
                    for perm in group['permissions']:
                        if isinstance(perm, dict) and 'id' in perm and perm.get('enabled', False):
                            permission_ids.append(perm['id'])
        
        return permission_ids
    
    def get_role_by_id(self, role_id: int):
        """Get role by ID with enhanced permission structure"""
        try:
            role = self.django_role_model.objects.prefetch_related('permissions').get(id=role_id)
            return role
        except self.django_role_model.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error getting role by ID: {e}")
            raise
    
    def get_roles(self, skip: int = 0, limit: int = 100, search: str = None):
        """Get roles with filtering and pagination"""
        try:
            from django.db import models
            
            queryset = self.django_role_model.objects.prefetch_related('permissions').all()
            
            # Apply filters
            if search:
                queryset = queryset.filter(
                    models.Q(name__icontains=search) |
                    models.Q(label__icontains=search)
                )
            
            # Apply pagination
            roles = list(queryset[skip:skip + limit])
            return roles
        except Exception as e:
            logger.error(f"Error getting roles: {e}")
            raise
    
    def create_role(self, role_data: Dict[str, Any]):
        """Create a new role with enhanced permission handling"""
        try:
            # Extract permission IDs from complex structure
            permission_ids = self._extract_permission_ids(role_data)
            
            # Check if role name already exists
            if self.django_role_model.objects.filter(name=role_data['name']).exists():
                return {
                    "status": "error",
                    "message": "Role with this name already exists"
                }
            
            # Create role
            role = self.django_role_model.objects.create(
                name=role_data['name'],
                label=role_data['label']
            )
            
            # Add permissions if provided
            if permission_ids:
                permissions = self.django_permission_model.objects.filter(
                    id__in=permission_ids
                )
                role.permissions.set(permissions)
            
            return {
                "status": "success",
                "message": "Role created successfully",
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
        except Exception as e:
            logger.error(f"Error creating role: {e}")
            return {
                "status": "error",
                "message": f"Failed to create role: {str(e)}"
            }
    
    def update_role(self, role_id: int, role_data: Dict[str, Any]):
        """Update role with enhanced permission handling"""
        try:
            role = self.django_role_model.objects.prefetch_related('permissions').get(id=role_id)
            
            # Extract permission IDs from complex structure
            permission_ids = self._extract_permission_ids(role_data)
            
            # Update basic fields
            if 'name' in role_data:
                role.name = role_data['name']
            if 'label' in role_data:
                role.label = role_data['label']
            
            # Update permissions if provided
            if permission_ids is not None:
                permissions = self.django_permission_model.objects.filter(
                    id__in=permission_ids
                )
                role.permissions.set(permissions)
            
            role.save()
            
            return {
                "status": "success",
                "message": "Role updated successfully",
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
        except self.django_role_model.DoesNotExist:
            return {
                "status": "error",
                "message": "Role not found"
            }
        except Exception as e:
            logger.error(f"Error updating role: {e}")
            return {
                "status": "error",
                "message": f"Failed to update role: {str(e)}"
            }
    
    def delete_role(self, role_id: int):
        """Delete role"""
        try:
            role = self.get_role_by_id(role_id)
            if not role:
                return {
                    "status": "error",
                    "message": "Role not found"
                }
            
            role.delete()
            return {
                "status": "success",
                "message": "Role deleted successfully"
            }
        except Exception as e:
            logger.error(f"Error deleting role: {e}")
            return {
                "status": "error",
                "message": f"Failed to delete role: {str(e)}"
            }
    
    def get_permissions(self):
        """Get all available permissions"""
        try:
            permissions = self.django_permission_model.objects.all()
            return {
                "status": "success",
                "data": [
                    {
                        "id": perm.id,
                        "name": perm.name,
                        "label": perm.label
                    } for perm in permissions
                ]
            }
        except Exception as e:
            logger.error(f"Error getting permissions: {e}")
            return {
                "status": "error",
                "message": f"Failed to retrieve permissions: {str(e)}"
            }
    
    def has_permission(self, user, permission_name: str) -> bool:
        """Check if user has specific permission"""
        try:
            # This would need to be implemented based on your user model and permission system
            return True  # Placeholder - implement based on your auth system
        except Exception as e:
            logger.error(f"Error checking permission: {e}")
            return False
