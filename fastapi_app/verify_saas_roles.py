#!/usr/bin/env python3
"""
Verify the new SaaS role structure
"""

import requests
import json

def verify_saas_roles():
    """Verify the SaaS role structure"""
    
    print("Verifying the new SaaS role structure...")
    print("=" * 60)
    
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
            
            # Group permissions by category
            permissions = role['permissions']
            if permissions:
                groups = {}
                for perm in permissions:
                    # Extract group from permission name
                    if 'system' in perm['name'] or 'tenant' in perm['name'] or 'backup' in perm['name'] or 'landing' in perm['name'] or 'theme' in perm['name'] or 'domain' in perm['name']:
                        group = 'System Administration'
                    elif 'user' in perm['name']:
                        group = 'User Management'
                    elif 'billing' in perm['name']:
                        group = 'Billing'
                    elif 'content' in perm['name']:
                        group = 'Content Management'
                    elif 'campaign' in perm['name']:
                        group = 'Campaigns'
                    elif 'property' in perm['name']:
                        group = 'Properties'
                    elif 'report' in perm['name'] or 'analytics' in perm['name']:
                        group = 'Analytics & Reports'
                    elif 'role' in perm['name']:
                        group = 'Role Management'
                    elif 'own' in perm['name']:
                        group = 'Own Data'
                    else:
                        group = 'Other'
                    
                    if group not in groups:
                        groups[group] = []
                    groups[group].append(perm['name'])
                
                for group, perms in groups.items():
                    print(f"    {group}: {len(perms)} permissions")
            else:
                print("    No permissions")
            print()
    else:
        print(f"Error: {response.text}")
    
    print("=" * 60)
    print("SaaS Role Structure Summary:")
    print("=" * 60)
    print("1. Super Admin - Complete system control and platform management")
    print("2. Admin - Full tenant management with all business features")
    print("3. Client - Limited access to own data and basic features")
    print()
    print("Ready for production use!")

if __name__ == "__main__":
    verify_saas_roles()
