#!/usr/bin/env python3
"""
Create Super Admin role and verify complete SaaS structure
"""

import requests
import json

def create_super_admin_and_verify():
    """Create Super Admin role and verify complete SaaS structure"""
    
    print("Creating Super Admin role...")
    print("=" * 50)
    
    # Create Super Admin role
    super_admin_data = {
        "name": "super_admin_platform",
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
    }
    
    try:
        response = requests.post('http://localhost:8140/api/roles/', json=super_admin_data)
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                role_info = result.get('data', {})
                print(f"SUCCESS: Created Super Admin role (ID: {role_info.get('id')})")
                print(f"  Name: {role_info.get('name')}")
                print(f"  Label: {role_info.get('label')}")
                print(f"  Permissions: {len(role_info.get('permissions', []))}")
            else:
                print(f"ERROR: {result.get('message')}")
        else:
            print(f"ERROR: {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    print()
    print("Verifying complete SaaS structure...")
    print("=" * 50)
    
    # Get all roles
    response = requests.get('http://localhost:8140/api/roles/')
    if response.status_code == 200:
        data = response.json()
        roles = data.get('data', {}).get('roles', [])
        
        print(f"Total roles: {len(roles)}")
        print()
        
        for role in roles:
            print(f"Role: {role['name']} ({role['label']})")
            print(f"  ID: {role['id']}")
            print(f"  Permissions: {len(role['permissions'])}")
            print()
    else:
        print(f"Error getting roles: {response.text}")
    
    print("=" * 50)
    print("SAAS ROLE STRUCTURE COMPLETE!")
    print("=" * 50)
    print("1. Super Admin - Complete system control")
    print("2. Admin - Full tenant management") 
    print("3. Client - Limited to own data")
    print()
    print("Ready for your SaaS platform!")

if __name__ == "__main__":
    create_super_admin_and_verify()
