#!/usr/bin/env python3
"""
Test script to debug permission table data structure.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8140"
API_BASE = f"{BASE_URL}/api"

def test_permission_table_debug():
    """Test and debug permission table data structure"""
    print("Testing Permission Table Debug")
    print("=" * 50)
    
    try:
        # Test 1: Get grouped permissions
        print("\n1. Testing GET /permissions/grouped/")
        response = requests.get(f"{API_BASE}/permissions/grouped/")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCCESS - Grouped permissions endpoint working")
            
            if 'data' in data and 'permission_groups' in data['data']:
                groups = data['data']['permission_groups']
                print(f"Found {len(groups)} permission groups")
                
                # Check first group structure
                if groups:
                    first_group = groups[0]
                    print(f"\nFirst group: {first_group['group']}")
                    print(f"Permissions in first group: {len(first_group['permissions'])}")
                    
                    if first_group['permissions']:
                        first_permission = first_group['permissions'][0]
                        print(f"First permission: {first_permission['name']}")
                        print(f"Has roles: {'roles' in first_permission}")
                        
                        if 'roles' in first_permission:
                            roles = first_permission['roles']
                            print(f"Number of role assignments: {len(roles)}")
                            print("Role assignments:")
                            for role in roles:
                                print(f"  - ID: {role['id']}, Name: {role['name']}, Enabled: {role['enabled']}")
                        else:
                            print("ERROR - No roles found in permission")
                            return False
                    else:
                        print("ERROR - No permissions found in first group")
                        return False
                else:
                    print("ERROR - No permission groups found")
                    return False
            else:
                print("ERROR - Invalid data structure")
                print(f"Response: {json.dumps(data, indent=2)}")
                return False
        else:
            print(f"ERROR - API call failed: {response.text}")
            return False
        
        print("\n" + "=" * 50)
        print("PERMISSION TABLE DEBUG SUCCESSFUL!")
        print("Data structure is correct for frontend table rendering")
        return True
        
    except Exception as e:
        print(f"ERROR - {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting Permission Table Debug Test")
    print(f"Testing against: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        if test_permission_table_debug():
            print("\nPermission table data structure is correct!")
            print("The frontend should be able to render the table with this data.")
        else:
            print("\nSome tests failed. Please check the output above.")
            
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
