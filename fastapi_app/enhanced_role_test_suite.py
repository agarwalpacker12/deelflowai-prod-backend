#!/usr/bin/env python3
"""
Comprehensive Test Suite for Enhanced Role Management
Tests complex permission structure with enabled booleans
"""

import requests
import json
import time
from typing import Dict, Any, List

class RoleManagementTester:
    def __init__(self, base_url: str = "http://localhost:8140"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None, 
                    expected_status: int = 200, test_name: str = "") -> Dict[str, Any]:
        """Make HTTP request and return response"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
            else:
                return {"error": f"Unsupported method: {method}"}
            
            result = {
                "test_name": test_name or f"{method} {endpoint}",
                "method": method,
                "endpoint": endpoint,
                "status": response.status_code,
                "expected": expected_status,
                "success": response.status_code == expected_status,
                "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            }
            
            self.test_results.append(result)
            return result
            
        except Exception as e:
            result = {
                "test_name": test_name or f"{method} {endpoint}",
                "method": method,
                "endpoint": endpoint,
                "status": "ERROR",
                "expected": expected_status,
                "success": False,
                "error": str(e)
            }
            self.test_results.append(result)
            return result
    
    def test_role_management(self):
        """Test comprehensive role management"""
        print("\n=== TESTING ENHANCED ROLE MANAGEMENT ===")
        
        # Test GET roles
        self.make_request("GET", "/api/roles/", test_name="Get Roles List")
        
        # Test GET permissions
        self.make_request("GET", "/api/roles/permissions/", test_name="Get Permissions List")
        
        # Test role creation with complex permission structure (your payload)
        unique_id = int(time.time())
        complex_role_payload = {
            "name": f"enhanced_test_role_{unique_id}",
            "label": f"Enhanced Test Role {unique_id}",
            "permissions": [
                {
                    "group": "Billing",
                    "count": "2 / 3",
                    "permissions": [
                        {"id": 5, "name": "manage_billing", "label": "Manage Billing", "enabled": True},
                        {"id": 6, "name": "view_billing", "label": "View Billing", "enabled": True}
                    ]
                },
                {
                    "group": "Users",
                    "count": "1 / 4",
                    "permissions": [
                        {"id": 1, "name": "create_users", "label": "Create Users", "enabled": True}
                    ]
                }
            ]
        }
        
        create_result = self.make_request("POST", "/api/roles/", complex_role_payload, 
                                        test_name="Create Role with Complex Permissions")
        
        # Test role creation with mixed enabled/disabled permissions
        unique_id_2 = int(time.time()) + 1
        mixed_role_payload = {
            "name": f"mixed_permissions_role_{unique_id_2}",
            "label": f"Mixed Permissions Role {unique_id_2}",
            "permissions": [
                {
                    "group": "Billing",
                    "count": "1 / 3",
                    "permissions": [
                        {"id": 5, "name": "manage_billing", "label": "Manage Billing", "enabled": True},
                        {"id": 6, "name": "view_billing", "label": "View Billing", "enabled": False},
                        {"id": 7, "name": "delete_billing", "label": "Delete Billing", "enabled": False}
                    ]
                }
            ]
        }
        
        self.make_request("POST", "/api/roles/", mixed_role_payload, 
                         test_name="Create Role with Mixed Enabled/Disabled Permissions")
        
        # Test role creation with empty permissions
        unique_id_3 = int(time.time()) + 2
        empty_permissions_payload = {
            "name": f"empty_permissions_role_{unique_id_3}",
            "label": f"Empty Permissions Role {unique_id_3}",
            "permissions": []
        }
        
        self.make_request("POST", "/api/roles/", empty_permissions_payload, 
                         test_name="Create Role with Empty Permissions")
        
        # Test role creation with invalid permission IDs
        unique_id_4 = int(time.time()) + 3
        invalid_permissions_payload = {
            "name": f"invalid_permissions_role_{unique_id_4}",
            "label": f"Invalid Permissions Role {unique_id_4}",
            "permissions": [
                {
                    "group": "Invalid",
                    "count": "1 / 1",
                    "permissions": [
                        {"id": 99999, "name": "invalid_permission", "label": "Invalid Permission", "enabled": True}
                    ]
                }
            ]
        }
        
        self.make_request("POST", "/api/roles/", invalid_permissions_payload, 
                         test_name="Create Role with Invalid Permission IDs")
        
        # Test role creation with missing required fields
        invalid_role_payload = {
            "name": "",  # Missing required field
            "label": "Invalid Role",
            "permissions": []
        }
        
        self.make_request("POST", "/api/roles/", invalid_role_payload, 
                         expected_status=400, test_name="Create Role with Missing Required Fields")
        
        # Test duplicate role creation
        self.make_request("POST", "/api/roles/", complex_role_payload, 
                         expected_status=400, test_name="Create Duplicate Role")
        
        # Test role update if we have a created role
        if create_result.get("success") and "data" in create_result.get("response", {}):
            role_id = create_result["response"]["data"]["id"]
            
            # Test GET specific role
            self.make_request("GET", f"/api/roles/{role_id}/", 
                             test_name="Get Specific Role")
            
            # Test role update with new permissions
            update_payload = {
                "name": f"updated_role_{unique_id}",
                "label": f"Updated Role {unique_id}",
                "permissions": [
                    {
                        "group": "Updated",
                        "count": "1 / 1",
                        "permissions": [
                            {"id": 1, "name": "create_users", "label": "Create Users", "enabled": True}
                        ]
                    }
                ]
            }
            
            self.make_request("PUT", f"/api/roles/{role_id}/", update_payload, 
                             test_name="Update Role with New Permissions")
        
        # Test role update with non-existent role
        self.make_request("PUT", "/api/roles/99999/", {"name": "test"}, 
                         expected_status=404, test_name="Update Non-existent Role")
        
        # Test role deletion with non-existent role
        self.make_request("DELETE", "/api/roles/99999/", 
                         expected_status=404, test_name="Delete Non-existent Role")
    
    def run_all_tests(self):
        """Run all comprehensive tests"""
        print("🚀 Starting Enhanced Role Management Test Suite...")
        
        # Wait for server to be ready
        time.sleep(3)
        
        # Run all test categories
        self.test_role_management()
        
        # Print results
        self.print_results()
    
    def print_results(self):
        """Print comprehensive test results"""
        print("\n" + "="*70)
        print("🎯 ENHANCED ROLE MANAGEMENT TEST RESULTS")
        print("="*70)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.get("success", False))
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result.get("success", False):
                    print(f"  {result['test_name']} - Status: {result['status']} (Expected: {result['expected']})")
                    if 'error' in result:
                        print(f"    Error: {result['error']}")
                    elif 'response' in result and isinstance(result['response'], dict):
                        print(f"    Response: {result['response']}")
        
        print("\n" + "="*70)
        
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED! Enhanced role management is fully functional!")
        else:
            print(f"⚠️  {failed_tests} tests failed. Review and fix issues.")

if __name__ == "__main__":
    tester = RoleManagementTester()
    tester.run_all_tests()
