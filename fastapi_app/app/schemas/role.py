"""
Enhanced Role and Permission related Pydantic schemas
Handles complex permission structure with enabled booleans
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

class PermissionBase(BaseModel):
    name: str
    label: str

class PermissionCreate(PermissionBase):
    pass

class PermissionResponse(PermissionBase):
    id: int
    enabled: Optional[bool] = None  # Add enabled field for frontend compatibility
    
    class Config:
        from_attributes = True

class PermissionWithEnabled(BaseModel):
    """Permission with enabled boolean for frontend"""
    id: int
    name: str
    label: str
    enabled: bool = False

class PermissionGroup(BaseModel):
    """Permission group structure from frontend"""
    group: str
    count: str
    permissions: List[PermissionWithEnabled]

class RoleBase(BaseModel):
    name: str
    label: str

class RoleCreate(RoleBase):
    """Enhanced role creation that handles both simple and complex permission structures"""
    permission_ids: Optional[List[int]] = []  # Simple list for backward compatibility
    permissions: Optional[List[PermissionGroup]] = None  # Complex nested structure
    
    def get_enabled_permission_ids(self) -> List[int]:
        """Extract enabled permission IDs from complex structure"""
        if self.permissions:
            enabled_ids = []
            for group in self.permissions:
                for perm in group.permissions:
                    if perm.enabled:
                        enabled_ids.append(perm.id)
            return enabled_ids
        return self.permission_ids or []

class RoleUpdate(BaseModel):
    """Enhanced role update that handles both simple and complex permission structures"""
    name: Optional[str] = None
    label: Optional[str] = None
    permission_ids: Optional[List[int]] = None  # Simple list for backward compatibility
    permissions: Optional[List[PermissionGroup]] = None  # Complex nested structure
    
    def get_enabled_permission_ids(self) -> List[int]:
        """Extract enabled permission IDs from complex structure"""
        if self.permissions:
            enabled_ids = []
            for group in self.permissions:
                for perm in group.permissions:
                    if perm.enabled:
                        enabled_ids.append(perm.id)
            return enabled_ids
        return self.permission_ids or []

class RoleResponse(RoleBase):
    """Enhanced role response with permission groups"""
    id: int
    permissions: List[PermissionResponse] = []
    permission_groups: Optional[List[PermissionGroup]] = None  # For frontend compatibility
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
    
    def to_frontend_format(self) -> Dict[str, Any]:
        """Convert to frontend-compatible format with permission groups"""
        # Group permissions by their natural grouping (this would need to be customized based on your permission structure)
        permission_groups = []
        
        # This is a simplified grouping - you might want to implement more sophisticated grouping
        if self.permissions:
            # Group by permission name prefix or implement custom grouping logic
            groups = {}
            for perm in self.permissions:
                # Simple grouping by permission name prefix
                group_name = perm.name.split('_')[0].title() if '_' in perm.name else 'General'
                if group_name not in groups:
                    groups[group_name] = []
                groups[group_name].append(PermissionWithEnabled(
                    id=perm.id,
                    name=perm.name,
                    label=perm.label,
                    enabled=True  # All permissions in response are enabled
                ))
            
            for group_name, perms in groups.items():
                permission_groups.append(PermissionGroup(
                    group=group_name,
                    count=f"{len(perms)} / {len(perms)}",  # This would need to be calculated based on total available permissions
                    permissions=perms
                ))
        
        return {
            "id": self.id,
            "name": self.name,
            "label": self.label,
            "permissions": permission_groups,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class RoleListResponse(BaseModel):
    roles: List[RoleResponse]
    total: int
    page: int
    limit: int
    has_next: bool = False
    has_prev: bool = False

class PermissionListResponse(BaseModel):
    permissions: List[PermissionResponse]
    total: int

class RoleCreateRequest(BaseModel):
    """Flexible role creation request that accepts both formats"""
    name: str
    label: str
    permissions: Optional[Union[List[int], List[PermissionGroup]]] = None
    
    def get_enabled_permission_ids(self) -> List[int]:
        """Extract enabled permission IDs from either format"""
        if not self.permissions:
            return []
        
        if isinstance(self.permissions[0], int):
            # Simple list format
            return self.permissions
        else:
            # Complex nested format
            enabled_ids = []
            for group in self.permissions:
                for perm in group.permissions:
                    if perm.enabled:
                        enabled_ids.append(perm.id)
            return enabled_ids
