#!/usr/bin/env python3
"""
Test script to verify the grouped permissions endpoint works correctly.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8140"
API_BASE = f"{BASE_URL}/api"

def test_grouped_permissions():
    """Test the grouped permissions endpoint"""
    print("Testing Grouped Permissions Endpoint")
    print("=" * 50)
    
    try:
        # Test the new grouped permissions endpoint
        response = requests.get(f"{API_BASE}/permissions/grouped/")
        print(f"GET /permissions/grouped/ - Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCCESS - Grouped permissions endpoint working")
            print(f"Response structure: {list(data.keys())}")
            
            if 'data' in data and 'permission_groups' in data['data']:
                groups = data['data']['permission_groups']
                print(f"Found {len(groups)} permission groups:")
                
                for group in groups:
                    print(f"  - {group['group']}: {len(group['permissions'])} permissions")
                    if group['permissions']:
                        first_perm = group['permissions'][0]
                        print(f"    Sample permission: {first_perm['name']}")
                        if 'roles' in first_perm:
                            print(f"    Has {len(first_perm['roles'])} role assignments")
                
                return True
            else:
                print("ERROR - Invalid response structure")
                return False
        else:
            print(f"ERROR - Status {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"ERROR - {str(e)}")
        return False

def test_regular_permissions():
    """Test the regular permissions endpoint for comparison"""
    print("\nTesting Regular Permissions Endpoint")
    print("=" * 50)
    
    try:
        response = requests.get(f"{API_BASE}/permissions/")
        print(f"GET /permissions/ - Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCCESS - Regular permissions endpoint working")
            if 'data' in data and 'permissions' in data['data']:
                print(f"Found {len(data['data']['permissions'])} permissions")
                return True
        else:
            print(f"ERROR - Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"ERROR - {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting Grouped Permissions Test")
    print(f"Testing against: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Test both endpoints
        regular_ok = test_regular_permissions()
        grouped_ok = test_grouped_permissions()
        
        if regular_ok and grouped_ok:
            print("\n" + "=" * 50)
            print("ALL TESTS PASSED!")
            print("Both permission endpoints are working correctly")
            print("The frontend can now use the grouped permissions endpoint")
        else:
            print("\n" + "=" * 50)
            print("SOME TESTS FAILED")
            print("Please check the output above for details")
            
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
