#!/usr/bin/env python
"""
Script to set up SaaS-specific roles for landing page, super admin, and customer
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

def create_saas_roles():
    """Create SaaS-specific roles based on the example provided"""
    
    # Get all permissions
    all_permissions = Permission.objects.all()
    
    # 1. Landing Page Role - Limited permissions for landing page management
    landing_page_permissions = all_permissions.filter(
        name__in=[
            "view_campaigns", "view_properties", "view_analytics", 
            "view_reports", "view_users", "view_billing"
        ]
    )
    
    landing_page_role, created = Role.objects.get_or_create(
        name="landing_page",
        defaults={"label": "Landing Page Manager"}
    )
    if created:
        landing_page_role.permissions.set(landing_page_permissions)
        print(f"+ Created Landing Page role with {landing_page_permissions.count()} permissions")
    else:
        print(f"- Landing Page role already exists")
    
    # 2. Super Admin Role - Full system access
    super_admin_role, created = Role.objects.get_or_create(
        name="super_admin",
        defaults={"label": "Super Admin"}
    )
    if created:
        super_admin_role.permissions.set(all_permissions)
        print(f"+ Created Super Admin role with {all_permissions.count()} permissions")
    else:
        print(f"- Super Admin role already exists")
    
    # 3. Customer Role - Limited access for customers
    customer_permissions = all_permissions.filter(
        name__in=[
            "view_campaigns", "view_properties", "view_analytics", 
            "view_reports", "view_billing", "create_campaigns", 
            "edit_campaigns", "create_properties", "view_users"
        ]
    )
    
    customer_role, created = Role.objects.get_or_create(
        name="customer",
        defaults={"label": "Customer"}
    )
    if created:
        customer_role.permissions.set(customer_permissions)
        print(f"+ Created Customer role with {customer_permissions.count()} permissions")
    else:
        print(f"- Customer role already exists")
    
    # 4. Client Panel Role - Similar to customer but with more permissions
    client_panel_permissions = all_permissions.filter(
        name__in=[
            "view_campaigns", "create_campaigns", "edit_campaigns", "view_campaigns",
            "view_properties", "create_properties", "edit_properties", "view_properties",
            "view_analytics", "view_reports", "export_reports", "view_billing",
            "view_users", "create_content", "edit_content"
        ]
    )
    
    client_panel_role, created = Role.objects.get_or_create(
        name="client_panel",
        defaults={"label": "Client Panel User"}
    )
    if created:
        client_panel_role.permissions.set(client_panel_permissions)
        print(f"+ Created Client Panel role with {client_panel_permissions.count()} permissions")
    else:
        print(f"- Client Panel role already exists")

def create_additional_permissions():
    """Create additional permissions specific to SaaS functionality"""
    
    additional_permissions = [
        # Landing Page specific
        {"name": "manage_landing_page", "label": "Manage Landing Page"},
        {"name": "customize_theme", "label": "Customize Theme"},
        {"name": "manage_domain", "label": "Manage Domain"},
        
        # Client Panel specific
        {"name": "manage_own_campaigns", "label": "Manage Own Campaigns"},
        {"name": "manage_own_properties", "label": "Manage Own Properties"},
        {"name": "view_own_analytics", "label": "View Own Analytics"},
        
        # Super Admin specific
        {"name": "manage_all_tenants", "label": "Manage All Tenants"},
        {"name": "system_settings", "label": "System Settings"},
        {"name": "backup_restore", "label": "Backup & Restore"},
    ]
    
    created_permissions = []
    for perm_data in additional_permissions:
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

def main():
    print("Setting up SaaS-specific roles...")
    print("=" * 50)
    
    # Create additional permissions
    print("\nCreating additional permissions...")
    additional_perms = create_additional_permissions()
    
    # Create SaaS roles
    print("\nCreating SaaS roles...")
    create_saas_roles()
    
    print("\n" + "=" * 50)
    print("SaaS role setup completed!")
    print(f"Total permissions: {Permission.objects.count()}")
    print(f"Total roles: {Role.objects.count()}")
    
    # Show SaaS role summary
    print("\nSaaS Role Summary:")
    saas_roles = ["landing_page", "super_admin", "customer", "client_panel"]
    for role_name in saas_roles:
        try:
            role = Role.objects.get(name=role_name)
            perm_count = role.permissions.count()
            print(f"  - {role.label} ({role.name}): {perm_count} permissions")
        except Role.DoesNotExist:
            print(f"  - {role_name}: Not found")

if __name__ == "__main__":
    main()
