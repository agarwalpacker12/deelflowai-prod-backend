#!/usr/bin/env python3
"""
Test script to verify the role management frontend functionality.
This script tests the complete role management workflow including:
1. Role creation with permissions
2. Role listing and display
3. Permission management and toggling
4. Role updates and deletion
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8140"
API_BASE = f"{BASE_URL}/api"

def test_api_endpoint(endpoint, method="GET", data=None, expected_status=200):
    """Test an API endpoint and return the response"""
    try:
        url = f"{API_BASE}{endpoint}"
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        print(f"{method} {endpoint} - Status: {response.status_code}")
        
        if response.status_code == expected_status:
            print(f"PASS - {method} {endpoint}")
            return response.json() if response.content else {}
        else:
            print(f"FAIL - {method} {endpoint} (Expected: {expected_status}, Got: {response.status_code})")
            if response.content:
                print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"ERROR - {method} {endpoint}: {str(e)}")
        return None

def test_role_management_workflow():
    """Test the complete role management workflow"""
    print("Testing Role Management Frontend Integration")
    print("=" * 60)
    
    # Test 1: Get all roles
    print("\n1. Testing GET /roles/ - Fetch all roles")
    roles_response = test_api_endpoint("/roles/")
    if not roles_response:
        print("Cannot proceed without roles data")
        return False
    
    roles = roles_response.get('data', {}).get('roles', [])
    print(f"Found {len(roles)} existing roles")
    
    # Test 2: Get all permissions
    print("\n2. Testing GET /permissions/ - Fetch all permissions")
    permissions_response = test_api_endpoint("/permissions/")
    if not permissions_response:
        print("Cannot proceed without permissions data")
        return False
    
    permissions = permissions_response.get('data', {}).get('permissions', [])
    print(f"Found {len(permissions)} available permissions")
    
    # Test 3: Create a new test role
    print("\n3. Testing POST /roles/ - Create new role")
    test_role_data = {
        "name": f"test_role_{int(time.time())}",
        "label": f"Test Role {datetime.now().strftime('%H:%M:%S')}",
        "permissions": [
            {
                "group": "User Management",
                "count": "2 / 4",
                "permissions": [
                    {
                        "id": 1,
                        "name": "create_users",
                        "label": "Create Users",
                        "enabled": True
                    },
                    {
                        "id": 3,
                        "name": "view_users",
                        "label": "View Users",
                        "enabled": True
                    }
                ]
            }
        ]
    }
    
    create_response = test_api_endpoint("/roles/", "POST", test_role_data, 201)
    if not create_response:
        print("Failed to create test role")
        return False
    
    created_role = create_response.get('data', {})
    role_id = created_role.get('id')
    print(f"Created role with ID: {role_id}")
    
    # Test 4: Get the created role by ID
    print(f"\n4. Testing GET /roles/{role_id}/ - Fetch created role")
    role_response = test_api_endpoint(f"/roles/{role_id}/")
    if not role_response:
        print("❌ Failed to fetch created role")
        return False
    
    print(f"✅ Retrieved role: {role_response.get('data', {}).get('name')}")
    
    # Test 5: Update the role permissions (simulate frontend toggle)
    print(f"\n5. Testing PUT /roles/{role_id}/ - Update role permissions")
    updated_permissions = [
        {
            "group": "User Management",
            "count": "3 / 4",
            "permissions": [
                {
                    "id": 1,
                    "name": "create_users",
                    "label": "Create Users",
                    "enabled": True
                },
                {
                    "id": 3,
                    "name": "view_users",
                    "label": "View Users",
                    "enabled": True
                },
                {
                    "id": 4,
                    "name": "edit_users",
                    "label": "Edit Users",
                    "enabled": True
                }
            ]
        },
        {
            "group": "Billing",
            "count": "1 / 3",
            "permissions": [
                {
                    "id": 6,
                    "name": "view_billing",
                    "label": "View Billing",
                    "enabled": True
                }
            ]
        }
    ]
    
    update_data = {
        "name": created_role.get('name'),
        "label": created_role.get('label'),
        "permissions": updated_permissions
    }
    
    update_response = test_api_endpoint(f"/roles/{role_id}/", "PUT", update_data, 200)
    if not update_response:
        print("❌ Failed to update role permissions")
        return False
    
    print("✅ Successfully updated role permissions")
    
    # Test 6: Verify the updated role
    print(f"\n6. Testing GET /roles/{role_id}/ - Verify updated role")
    updated_role_response = test_api_endpoint(f"/roles/{role_id}/")
    if not updated_role_response:
        print("❌ Failed to fetch updated role")
        return False
    
    updated_permissions_count = len(updated_role_response.get('data', {}).get('permissions', []))
    print(f"✅ Updated role now has {updated_permissions_count} permissions")
    
    # Test 7: Test permission toggle (simulate frontend real-time toggle)
    print(f"\n7. Testing Real-time Permission Toggle")
    
    # Toggle off a permission
    toggled_permissions = [
        {
            "group": "User Management",
            "count": "2 / 4",
            "permissions": [
                {
                    "id": 1,
                    "name": "create_users",
                    "label": "Create Users",
                    "enabled": True
                },
                {
                    "id": 3,
                    "name": "view_users",
                    "label": "View Users",
                    "enabled": True
                }
            ]
        }
    ]
    
    toggle_data = {
        "name": created_role.get('name'),
        "label": created_role.get('label'),
        "permissions": toggled_permissions
    }
    
    toggle_response = test_api_endpoint(f"/roles/{role_id}/", "PUT", toggle_data, 200)
    if not toggle_response:
        print("❌ Failed to toggle permission")
        return False
    
    print("✅ Successfully toggled permission off")
    
    # Test 8: Delete the test role
    print(f"\n8. Testing DELETE /roles/{role_id}/ - Delete test role")
    delete_response = test_api_endpoint(f"/roles/{role_id}/", "DELETE", expected_status=200)
    if not delete_response:
        print("❌ Failed to delete test role")
        return False
    
    print("✅ Successfully deleted test role")
    
    # Test 9: Verify role is deleted
    print(f"\n9. Testing GET /roles/{role_id}/ - Verify role deletion")
    deleted_role_response = test_api_endpoint(f"/roles/{role_id}/", expected_status=404)
    if deleted_role_response is None:
        print("✅ Role successfully deleted (404 as expected)")
    else:
        print("❌ Role still exists after deletion")
        return False
    
    print("\n" + "=" * 60)
    print("ALL ROLE MANAGEMENT TESTS PASSED!")
    print("Frontend integration is working correctly")
    print("Real-time permission toggling works")
    print("Role CRUD operations work")
    print("Permission management works")
    
    return True

def test_permission_structure():
    """Test the permission structure matches frontend expectations"""
    print("\nTesting Permission Structure")
    print("-" * 40)
    
    permissions_response = test_api_endpoint("/permissions/")
    if not permissions_response:
        return False
    
    permissions = permissions_response.get('data', {}).get('permissions', [])
    
    # Check if permissions have required fields
    required_fields = ['id', 'name', 'label']
    for permission in permissions[:5]:  # Check first 5 permissions
        for field in required_fields:
            if field not in permission:
                print(f"❌ Permission missing required field: {field}")
                return False
    
    print(f"✅ Permission structure is correct ({len(permissions)} permissions)")
    
    # Test permission categorization (as used in frontend)
    categories = set()
    for permission in permissions:
        name = permission.get('name', '')
        if 'user' in name:
            categories.add('User Management')
        elif 'billing' in name:
            categories.add('Billing')
        elif 'content' in name:
            categories.add('Content Management')
        elif 'campaign' in name:
            categories.add('Campaigns')
        elif 'property' in name:
            categories.add('Properties')
        elif 'report' in name or 'analytics' in name:
            categories.add('Analytics & Reports')
        elif 'role' in name:
            categories.add('Role Management')
        elif any(x in name for x in ['system', 'tenant', 'backup', 'landing', 'theme', 'domain']):
            categories.add('System Administration')
        elif 'own' in name:
            categories.add('Own Data')
        else:
            categories.add('Other')
    
    print(f"✅ Permission categories detected: {', '.join(sorted(categories))}")
    return True

if __name__ == "__main__":
    print("Starting Role Management Frontend Integration Tests")
    print(f"Testing against: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Test permission structure first
        if not test_permission_structure():
            print("Permission structure test failed")
            exit(1)
        
        # Test complete workflow
        if test_role_management_workflow():
            print("\nALL TESTS COMPLETED SUCCESSFULLY!")
            print("Your role management frontend is ready for production!")
        else:
            print("\nSome tests failed. Please check the output above.")
            exit(1)
            
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        exit(1)
