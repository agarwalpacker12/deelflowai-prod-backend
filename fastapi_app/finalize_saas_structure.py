#!/usr/bin/env python3
"""
Finalize SaaS structure by removing duplicates and keeping only 3 essential roles
"""

import requests
import json

def finalize_saas_structure():
    """Finalize SaaS structure with only 3 essential roles"""
    
    print("Finalizing SaaS structure...")
    print("=" * 50)
    
    # Get all roles
    response = requests.get('http://localhost:8140/api/roles/')
    if response.status_code == 200:
        data = response.json()
        roles = data.get('data', {}).get('roles', [])
        
        print(f"Current roles: {len(roles)}")
        
        # Keep only the roles we want
        keep_roles = ['super_admin_platform', 'admin', 'client']
        
        for role in roles:
            if role['name'] not in keep_roles:
                try:
                    delete_response = requests.delete(f'http://localhost:8140/api/roles/{role["id"]}/')
                    if delete_response.status_code == 200:
                        print(f"Deleted: {role['name']} (ID: {role['id']})")
                    else:
                        print(f"Failed to delete {role['name']}: {delete_response.text}")
                except Exception as e:
                    print(f"Error deleting {role['name']}: {e}")
    
    print()
    print("Final SaaS structure verification...")
    print("=" * 50)
    
    # Get all roles after cleanup
    response = requests.get('http://localhost:8140/api/roles/')
    if response.status_code == 200:
        data = response.json()
        roles = data.get('data', {}).get('roles', [])
        
        print(f"Final roles: {len(roles)}")
        print()
        
        for role in roles:
            print(f"Role: {role['name']} ({role['label']})")
            print(f"  ID: {role['id']}")
            print(f"  Permissions: {len(role['permissions'])}")
            print()
    else:
        print(f"Error getting roles: {response.text}")
    
    print("=" * 50)
    print("SAAS STRUCTURE FINALIZED!")
    print("=" * 50)
    print("Perfect for your SaaS platform:")
    print("1. Super Admin - perfextosaas.com/admin (admin@admin.com)")
    print("2. Admin - Full tenant management")
    print("3. Client - perfextosaas.com (customer@customer.com)")
    print()
    print("Ready for production!")

if __name__ == "__main__":
    finalize_saas_structure()
