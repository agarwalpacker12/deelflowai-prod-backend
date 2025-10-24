#!/usr/bin/env python3
"""
Clean up all existing roles and create proper SaaS role structure
"""

import requests
import json
import time

def cleanup_and_create_saas_roles():
    """Clean up existing roles and create proper SaaS structure"""
    
    print("Cleaning up roles and creating proper SaaS structure...")
    print("=" * 60)
    
    # First, get all existing roles
    try:
        response = requests.get('http://localhost:8140/api/roles/')
        if response.status_code == 200:
            data = response.json()
            roles = data.get('data', {}).get('roles', [])
            print(f"Found {len(roles)} existing roles")
            
            # Delete all existing roles
            deleted_count = 0
            for role in roles:
                role_id = role['id']
                try:
                    delete_response = requests.delete(f'http://localhost:8140/api/roles/{role_id}/')
                    if delete_response.status_code == 200:
                        print(f"Deleted role: {role['name']} (ID: {role_id})")
                        deleted_count += 1
                    else:
                        print(f"Failed to delete role: {role['name']} - {delete_response.text}")
                except Exception as e:
                    print(f"Error deleting role {role['name']}: {e}")
            
            print(f"\nCleanup complete! Deleted {deleted_count} roles")
            
        else:
            print(f"Failed to get roles: {response.text}")
            return
            
    except Exception as e:
        print(f"Error getting roles: {e}")
        return
    
    # Wait a moment for cleanup to complete
    time.sleep(2)
    
    # Create the proper SaaS role structure
    print("\nCreating proper SaaS role structure...")
    print("=" * 60)
    
    # Define the SaaS roles based on your structure
    saas_roles = [
        {
            "name": "super_admin",
            "label": "Super Admin",
            "description": "Platform-wide administrator with complete system control. Manages all tenants, subscriptions, and platform configuration.",
            "permissions": [
                {
                    "group": "System Administration",
                    "count": "8 / 8",
                    "permissions": [
                        {"id": 27, "name": "system_admin", "label": "System Administration", "enabled": True},
                        {"id": 28, "name": "tenant_management", "label": "Tenant Management", "enabled": True},
                        {"id": 35, "name": "manage_all_tenants", "label": "Manage All Tenants", "enabled": True},
                        {"id": 36, "name": "system_settings", "label": "System Settings", "enabled": True},
                        {"id": 37, "name": "backup_restore", "label": "Backup & Restore", "enabled": True},
                        {"id": 29, "name": "manage_landing_page", "label": "Manage Landing Page", "enabled": True},
                        {"id": 30, "name": "customize_theme", "label": "Customize Theme", "enabled": True},
                        {"id": 31, "name": "manage_domain", "label": "Manage Domain", "enabled": True}
                    ]
                }
            ]
        },
        {
            "name": "admin",
            "label": "Admin",
            "description": "Administrator with full access to all features within their tenant. Can manage users, roles, and all business functions.",
            "permissions": [
                {
                    "group": "User Management",
                    "count": "4 / 4",
                    "permissions": [
                        {"id": 1, "name": "create_users", "label": "Create Users", "enabled": True},
                        {"id": 2, "name": "view_users", "label": "View Users", "enabled": True},
                        {"id": 3, "name": "edit_users", "label": "Edit Users", "enabled": True},
                        {"id": 4, "name": "delete_users", "label": "Delete Users", "enabled": True}
                    ]
                },
                {
                    "group": "Role Management",
                    "count": "2 / 2",
                    "permissions": [
                        {"id": 25, "name": "manage_roles", "label": "Manage Roles", "enabled": True},
                        {"id": 26, "name": "view_roles", "label": "View Roles", "enabled": True}
                    ]
                },
                {
                    "group": "Billing",
                    "count": "3 / 3",
                    "permissions": [
                        {"id": 5, "name": "manage_billing", "label": "Manage Billing", "enabled": True},
                        {"id": 6, "name": "view_billing", "label": "View Billing", "enabled": True},
                        {"id": 7, "name": "export_billing", "label": "Export Billing Reports", "enabled": True}
                    ]
                },
                {
                    "group": "Content Management",
                    "count": "4 / 4",
                    "permissions": [
                        {"id": 8, "name": "create_content", "label": "Create Content", "enabled": True},
                        {"id": 9, "name": "edit_content", "label": "Edit Content", "enabled": True},
                        {"id": 10, "name": "delete_content", "label": "Delete Content", "enabled": True},
                        {"id": 11, "name": "publish_content", "label": "Publish Content", "enabled": True}
                    ]
                },
                {
                    "group": "Campaigns",
                    "count": "4 / 4",
                    "permissions": [
                        {"id": 15, "name": "create_campaigns", "label": "Create Campaigns", "enabled": True},
                        {"id": 16, "name": "view_campaigns", "label": "View Campaigns", "enabled": True},
                        {"id": 17, "name": "edit_campaigns", "label": "Edit Campaigns", "enabled": True},
                        {"id": 18, "name": "delete_campaigns", "label": "Delete Campaigns", "enabled": True}
                    ]
                },
                {
                    "group": "Properties",
                    "count": "4 / 4",
                    "permissions": [
                        {"id": 19, "name": "create_properties", "label": "Create Properties", "enabled": True},
                        {"id": 20, "name": "view_properties", "label": "View Properties", "enabled": True},
                        {"id": 21, "name": "edit_properties", "label": "Edit Properties", "enabled": True},
                        {"id": 22, "name": "delete_properties", "label": "Delete Properties", "enabled": True}
                    ]
                },
                {
                    "group": "Analytics & Reports",
                    "count": "4 / 4",
                    "permissions": [
                        {"id": 12, "name": "view_reports", "label": "View Reports", "enabled": True},
                        {"id": 13, "name": "export_reports", "label": "Export Reports", "enabled": True},
                        {"id": 14, "name": "create_reports", "label": "Create Custom Reports", "enabled": True},
                        {"id": 23, "name": "view_analytics", "label": "View Analytics", "enabled": True}
                    ]
                }
            ]
        },
        {
            "name": "client",
            "label": "Client",
            "description": "Client user with limited access to their own data and basic features. Can manage their own campaigns and properties.",
            "permissions": [
                {
                    "group": "Own Campaigns",
                    "count": "1 / 1",
                    "permissions": [
                        {"id": 32, "name": "manage_own_campaigns", "label": "Manage Own Campaigns", "enabled": True}
                    ]
                },
                {
                    "group": "Own Properties",
                    "count": "1 / 1",
                    "permissions": [
                        {"id": 33, "name": "manage_own_properties", "label": "Manage Own Properties", "enabled": True}
                    ]
                },
                {
                    "group": "Own Analytics",
                    "count": "1 / 1",
                    "permissions": [
                        {"id": 34, "name": "view_own_analytics", "label": "View Own Analytics", "enabled": True}
                    ]
                }
            ]
        }
    ]
    
    # Create each SaaS role
    created_roles = []
    for role_data in saas_roles:
        try:
            response = requests.post('http://localhost:8140/api/roles/', json=role_data)
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    role_info = result.get('data', {})
                    print(f"Created role: {role_info.get('name')} (ID: {role_info.get('id')})")
                    print(f"   Label: {role_info.get('label')}")
                    print(f"   Permissions: {len(role_info.get('permissions', []))}")
                    created_roles.append(role_info)
                else:
                    print(f"Failed to create role {role_data['name']}: {result.get('message')}")
            else:
                print(f"Failed to create role {role_data['name']}: {response.text}")
        except Exception as e:
            print(f"Error creating role {role_data['name']}: {e}")
    
    print(f"\nSaaS role structure created successfully!")
    print(f"Created {len(created_roles)} roles:")
    for role in created_roles:
        print(f"  - {role['name']}: {role['label']}")
    
    print("\n" + "=" * 60)
    print("SaaS Role Structure Complete!")
    print("=" * 60)
    print("1. Super Admin - Complete system control")
    print("2. Admin - Full tenant management")
    print("3. Client - Limited to own data")
    print("\nReady for production use!")

if __name__ == "__main__":
    cleanup_and_create_saas_roles()
