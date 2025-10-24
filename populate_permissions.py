#!/usr/bin/env python
"""
Script to populate the database with default permissions and roles
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deelflow.settings')
django.setup()

from deelflow.models import Permission, Role

def create_permissions():
    """Create default permissions based on the UI structure"""
    
    permissions_data = [
        # User Management
        {"name": "create_users", "label": "Create Users"},
        {"name": "view_users", "label": "View Users"},
        {"name": "edit_users", "label": "Edit Users"},
        {"name": "delete_users", "label": "Delete Users"},
        
        # Billing
        {"name": "manage_billing", "label": "Manage Billing"},
        {"name": "view_billing", "label": "View Billing"},
        {"name": "export_billing", "label": "Export Billing Reports"},
        
        # Content Management
        {"name": "create_content", "label": "Create Content"},
        {"name": "edit_content", "label": "Edit Content"},
        {"name": "delete_content", "label": "Delete Content"},
        {"name": "publish_content", "label": "Publish Content"},
        
        # Reports
        {"name": "view_reports", "label": "View Reports"},
        {"name": "export_reports", "label": "Export Reports"},
        {"name": "create_reports", "label": "Create Custom Reports"},
        
        # Campaign Management
        {"name": "create_campaigns", "label": "Create Campaigns"},
        {"name": "view_campaigns", "label": "View Campaigns"},
        {"name": "edit_campaigns", "label": "Edit Campaigns"},
        {"name": "delete_campaigns", "label": "Delete Campaigns"},
        
        # Property Management
        {"name": "create_properties", "label": "Create Properties"},
        {"name": "view_properties", "label": "View Properties"},
        {"name": "edit_properties", "label": "Edit Properties"},
        {"name": "delete_properties", "label": "Delete Properties"},
        
        # Analytics
        {"name": "view_analytics", "label": "View Analytics"},
        {"name": "export_analytics", "label": "Export Analytics"},
        
        # Role Management
        {"name": "manage_roles", "label": "Manage Roles"},
        {"name": "view_roles", "label": "View Roles"},
        
        # System Administration
        {"name": "system_admin", "label": "System Administration"},
        {"name": "tenant_management", "label": "Tenant Management"},
    ]
    
    created_permissions = []
    for perm_data in permissions_data:
        permission, created = Permission.objects.get_or_create(
            name=perm_data["name"],
            defaults={"label": perm_data["label"]}
        )
        created_permissions.append(permission)
        if created:
            print(f"+ Created permission: {permission.name} - {permission.label}")
        else:
            print(f"- Permission already exists: {permission.name} - {permission.label}")
    
    return created_permissions

def create_default_roles():
    """Create default roles with permissions"""
    
    # Get all permissions
    all_permissions = Permission.objects.all()
    
    # Admin role - all permissions
    admin_role, created = Role.objects.get_or_create(
        name="admin",
        defaults={"label": "Administrator"}
    )
    if created:
        admin_role.permissions.set(all_permissions)
        print(f"+ Created admin role with {all_permissions.count()} permissions")
    else:
        print(f"- Admin role already exists")
    
    # Content Manager role
    content_permissions = all_permissions.filter(
        name__in=["create_content", "edit_content", "delete_content", "publish_content", 
                 "view_users", "view_reports", "view_analytics"]
    )
    content_manager_role, created = Role.objects.get_or_create(
        name="content_manager",
        defaults={"label": "Content Manager"}
    )
    if created:
        content_manager_role.permissions.set(content_permissions)
        print(f"+ Created content manager role with {content_permissions.count()} permissions")
    else:
        print(f"- Content Manager role already exists")
    
    # Campaign Manager role
    campaign_permissions = all_permissions.filter(
        name__in=["create_campaigns", "view_campaigns", "edit_campaigns", "delete_campaigns",
                 "view_properties", "view_analytics", "view_reports"]
    )
    campaign_manager_role, created = Role.objects.get_or_create(
        name="campaign_manager",
        defaults={"label": "Campaign Manager"}
    )
    if created:
        campaign_manager_role.permissions.set(campaign_permissions)
        print(f"+ Created campaign manager role with {campaign_permissions.count()} permissions")
    else:
        print(f"- Campaign Manager role already exists")
    
    # Viewer role - read-only
    viewer_permissions = all_permissions.filter(
        name__in=["view_users", "view_campaigns", "view_properties", "view_analytics", 
                 "view_reports", "view_billing"]
    )
    viewer_role, created = Role.objects.get_or_create(
        name="viewer",
        defaults={"label": "Viewer"}
    )
    if created:
        viewer_role.permissions.set(viewer_permissions)
        print(f"+ Created viewer role with {viewer_permissions.count()} permissions")
    else:
        print(f"- Viewer role already exists")
    
    # Billing Manager role
    billing_permissions = all_permissions.filter(
        name__in=["manage_billing", "view_billing", "export_billing", "view_reports", "export_reports"]
    )
    billing_manager_role, created = Role.objects.get_or_create(
        name="billing_manager",
        defaults={"label": "Billing Manager"}
    )
    if created:
        billing_manager_role.permissions.set(billing_permissions)
        print(f"+ Created billing manager role with {billing_permissions.count()} permissions")
    else:
        print(f"- Billing Manager role already exists")

def main():
    print("Populating permissions and roles...")
    print("=" * 50)
    
    # Create permissions
    print("\nCreating permissions...")
    permissions = create_permissions()
    
    # Create default roles
    print("\nCreating default roles...")
    create_default_roles()
    
    print("\n" + "=" * 50)
    print("Database population completed!")
    print(f"Total permissions: {Permission.objects.count()}")
    print(f"Total roles: {Role.objects.count()}")
    
    # Show role summary
    print("\nRole Summary:")
    for role in Role.objects.all():
        perm_count = role.permissions.count()
        print(f"  - {role.label} ({role.name}): {perm_count} permissions")

if __name__ == "__main__":
    main()
