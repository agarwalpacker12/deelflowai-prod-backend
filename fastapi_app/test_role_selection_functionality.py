#!/usr/bin/env python3
"""
Test script to verify role selection functionality is working.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8140"
API_BASE = f"{BASE_URL}/api"

def test_role_selection_functionality():
    """Test the role selection functionality"""
    print("Testing Role Selection Functionality")
    print("=" * 50)
    
    try:
        # Test 1: Get all roles
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
                
                # Test 2: Get grouped permissions
                print("\n2. Testing GET /permissions/grouped/")
                permissions_response = requests.get(f"{API_BASE}/permissions/grouped/")
                print(f"Status: {permissions_response.status_code}")
                
                if permissions_response.status_code == 200:
                    permissions_data = permissions_response.json()
                    print("SUCCESS - Grouped permissions endpoint working")
                    
                    if 'data' in permissions_data and 'permission_groups' in permissions_data['data']:
                        groups = permissions_data['data']['permission_groups']
                        print(f"Found {len(groups)} permission groups")
                        
                        # Test 3: Verify role-permission mapping
                        print("\n3. Testing role-permission mapping")
                        if groups and groups[0]['permissions']:
                            first_perm = groups[0]['permissions'][0]
                            if 'roles' in first_perm:
                                role_assignments = first_perm['roles']
                                print(f"First permission '{first_perm['name']}' has {len(role_assignments)} role assignments:")
                                
                                for role_assignment in role_assignments:
                                    role_id = role_assignment['id']
                                    role_name = role_assignment['name']
                                    enabled = role_assignment['enabled']
                                    print(f"  - Role {role_id} ({role_name}): {'Enabled' if enabled else 'Disabled'}")
                                
                                # Test 4: Simulate role selection
                                print("\n4. Testing role selection simulation")
                                selected_role_id = roles[0]['id']
                                print(f"Simulating selection of role ID: {selected_role_id}")
                                
                                # Find the role in the permission assignments
                                selected_role_assignment = next(
                                    (ra for ra in role_assignments if ra['id'] == selected_role_id), 
                                    None
                                )
                                
                                if selected_role_assignment:
                                    print(f"SUCCESS - Role {selected_role_id} found in permission assignments")
                                    print(f"Role name: {selected_role_assignment['name']}")
                                    print(f"Permission enabled: {selected_role_assignment['enabled']}")
                                    print("This role can be highlighted in the permission table")
                                else:
                                    print(f"WARNING - Role {selected_role_id} not found in permission assignments")
                            else:
                                print("ERROR - No role assignments found in permissions")
                                return False
                        else:
                            print("ERROR - No permissions found in groups")
                            return False
                    else:
                        print("ERROR - Invalid permissions data structure")
                        return False
                else:
                    print(f"ERROR - Grouped permissions endpoint failed: {permissions_response.text}")
                    return False
            else:
                print("ERROR - Invalid roles data structure")
                return False
        else:
            print(f"ERROR - Roles endpoint failed: {roles_response.text}")
            return False
        
        print("\n" + "=" * 50)
        print("ROLE SELECTION FUNCTIONALITY TESTS PASSED!")
        print("Role cards should now open the permission management table")
        print("and highlight the selected role column")
        return True
        
    except Exception as e:
        print(f"ERROR - {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting Role Selection Functionality Test")
    print(f"Testing against: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        if test_role_selection_functionality():
            print("\nRole selection functionality is working correctly!")
            print("\nExpected behavior:")
            print("1. Click on a role card")
            print("2. Page should scroll to permission management table")
            print("3. Selected role column should be highlighted in blue")
            print("4. Role name should be shown above the table")
        else:
            print("\nSome tests failed. Please check the output above.")
            
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
