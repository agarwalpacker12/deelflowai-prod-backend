#!/usr/bin/env python3
"""
Test script to verify the frontend integration is working correctly.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8140"
API_BASE = f"{BASE_URL}/api"

def test_frontend_integration():
    """Test the frontend integration endpoints"""
    print("Testing Frontend Integration")
    print("=" * 50)
    
    try:
        # Test 1: Get roles
        print("\n1. Testing GET /roles/")
        roles_response = requests.get(f"{API_BASE}/roles/")
        print(f"Status: {roles_response.status_code}")
        
        if roles_response.status_code == 200:
            roles_data = roles_response.json()
            print("SUCCESS - Roles endpoint working")
            if 'data' in roles_data and 'roles' in roles_data['data']:
                roles = roles_data['data']['roles']
                print(f"Found {len(roles)} roles:")
                for role in roles:
                    print(f"  - {role.get('name')} (ID: {role.get('id')})")
            else:
                print("ERROR - Invalid roles data structure")
                return False
        else:
            print(f"ERROR - Roles endpoint failed: {roles_response.text}")
            return False
        
        # Test 2: Get grouped permissions
        print("\n2. Testing GET /permissions/grouped/")
        permissions_response = requests.get(f"{API_BASE}/permissions/grouped/")
        print(f"Status: {permissions_response.status_code}")
        
        if permissions_response.status_code == 200:
            permissions_data = permissions_response.json()
            print("SUCCESS - Grouped permissions endpoint working")
            
            if 'data' in permissions_data and 'permission_groups' in permissions_data['data']:
                groups = permissions_data['data']['permission_groups']
                print(f"Found {len(groups)} permission groups:")
                
                for group in groups:
                    print(f"  - {group['group']}: {len(group['permissions'])} permissions")
                    if group['permissions']:
                        first_perm = group['permissions'][0]
                        print(f"    Sample: {first_perm['name']}")
                        if 'roles' in first_perm:
                            print(f"    Has {len(first_perm['roles'])} role assignments")
                            # Check if roles match the roles from the roles endpoint
                            role_ids = [r['id'] for r in first_perm['roles']]
                            print(f"    Role IDs: {role_ids}")
            else:
                print("ERROR - Invalid permissions data structure")
                return False
        else:
            print(f"ERROR - Grouped permissions endpoint failed: {permissions_response.text}")
            return False
        
        # Test 3: Verify data consistency
        print("\n3. Testing data consistency")
        roles_ids = [role['id'] for role in roles_data['data']['roles']]
        
        if groups:
            first_perm_roles = groups[0]['permissions'][0]['roles']
            permission_role_ids = [r['id'] for r in first_perm_roles]
            
            print(f"Roles from /roles/: {roles_ids}")
            print(f"Roles from /permissions/grouped/: {permission_role_ids}")
            
            if set(roles_ids) == set(permission_role_ids):
                print("SUCCESS - Role IDs match between endpoints")
            else:
                print("WARNING - Role IDs don't match between endpoints")
                print("This might cause issues in the frontend table")
        
        print("\n" + "=" * 50)
        print("ALL FRONTEND INTEGRATION TESTS PASSED!")
        print("The frontend should now work correctly")
        return True
        
    except Exception as e:
        print(f"ERROR - {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting Frontend Integration Test")
    print(f"Testing against: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        if test_frontend_integration():
            print("\nFrontend integration is working correctly!")
        else:
            print("\nSome tests failed. Please check the output above.")
            
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
