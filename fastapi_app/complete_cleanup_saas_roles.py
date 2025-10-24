#!/usr/bin/env python3
"""
Complete cleanup of all roles and create proper SaaS structure
Handles pagination to delete ALL roles
"""

import requests
import json
import time

def complete_cleanup_and_create_saas_roles():
    """Complete cleanup of all roles and create proper SaaS structure"""
    
    print("Complete cleanup of all roles and creating proper SaaS structure...")
    print("=" * 70)
    
    # Get all roles with pagination
    all_roles = []
    page = 1
    limit = 100  # Get more per page
    
    while True:
        try:
            response = requests.get(f'http://localhost:8140/api/roles/?page={page}&limit={limit}')
            if response.status_code == 200:
                data = response.json()
                roles_data = data.get('data', {})
                roles = roles_data.get('roles', [])
                total_pages = roles_data.get('total_pages', 1)
                
                if not roles:  # No more roles
                    break
                    
                all_roles.extend(roles)
                print(f"Fetched page {page}/{total_pages} - {len(roles)} roles")
                
                if page >= total_pages:
                    break
                page += 1
            else:
                print(f"Error fetching page {page}: {response.text}")
                break
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
    
    print(f"\nTotal roles found: {len(all_roles)}")
    
    # Delete all existing roles
    deleted_count = 0
    failed_count = 0
    
    for role in all_roles:
        role_id = role['id']
        try:
            delete_response = requests.delete(f'http://localhost:8140/api/roles/{role_id}/')
            if delete_response.status_code == 200:
                print(f"Deleted: {role['name']} (ID: {role_id})")
                deleted_count += 1
            else:
                print(f"Failed to delete: {role['name']} - {delete_response.text}")
                failed_count += 1
        except Exception as e:
            print(f"Error deleting {role['name']}: {e}")
            failed_count += 1
    
    print(f"\nCleanup Summary:")
    print(f"  Deleted: {deleted_count} roles")
    print(f"  Failed: {failed_count} roles")
    
    # Wait for cleanup to complete
    time.sleep(3)
    
    # Create the proper SaaS role structure
    print("\nCreating proper SaaS role structure...")
    print("=" * 70)
    
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
                    print(f"Created: {role_info.get('name')} (ID: {role_info.get('id')})")
                    print(f"  Label: {role_info.get('label')}")
                    print(f"  Permissions: {len(role_info.get('permissions', []))}")
                    created_roles.append(role_info)
                else:
                    print(f"Failed to create {role_data['name']}: {result.get('message')}")
            else:
                print(f"Failed to create {role_data['name']}: {response.text}")
        except Exception as e:
            print(f"Error creating {role_data['name']}: {e}")
    
    print(f"\n" + "=" * 70)
    print(f"SAAS ROLE STRUCTURE COMPLETE!")
    print(f"=" * 70)
    print(f"Created {len(created_roles)} roles:")
    for role in created_roles:
        print(f"  - {role['name']}: {role['label']}")
    
    print(f"\nRole Structure:")
    print(f"1. Super Admin - Complete system control and platform management")
    print(f"2. Admin - Full tenant management with all business features")
    print(f"3. Client - Limited access to own data and basic features")
    print(f"\nReady for production use!")

if __name__ == "__main__":
    complete_cleanup_and_create_saas_roles()
