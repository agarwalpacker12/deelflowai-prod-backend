#!/usr/bin/env python3
"""
Frontend-Backend Integration Test
Tests the complete integration between frontend and backend
"""

import requests
import json
import time
import sys

class FrontendBackendIntegrationTester:
    def __init__(self, base_url="http://localhost:8140"):
        self.base_url = base_url
        self.test_results = []
        
    def test_endpoint(self, method, endpoint, expected_status=200, data=None, description=""):
        """Test a single endpoint"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == "GET":
                response = requests.get(url)
            elif method.upper() == "POST":
                response = requests.post(url, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            success = response.status_code == expected_status
            result = {
                "method": method,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "success": success,
                "description": description,
                "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text[:200]
            }
            
            self.test_results.append(result)
            return result
            
        except Exception as e:
            result = {
                "method": method,
                "endpoint": endpoint,
                "status_code": "ERROR",
                "expected_status": expected_status,
                "success": False,
                "description": description,
                "error": str(e)
            }
            self.test_results.append(result)
            return result
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("🚀 Starting Frontend-Backend Integration Tests...")
        print("=" * 60)
        
        # Test 1: Basic server connectivity
        print("\n1. Testing Server Connectivity...")
        self.test_endpoint("GET", "/docs", 200, description="Swagger documentation")
        self.test_endpoint("GET", "/openapi.json", 200, description="OpenAPI schema")
        
        # Test 2: Main API endpoints (working)
        print("\n2. Testing Main API Endpoints...")
        self.test_endpoint("GET", "/api/roles/", 200, description="Get all roles")
        self.test_endpoint("GET", "/api/permissions/", 200, description="Get all permissions")
        
        # Test 3: Legacy endpoints (should work after our fixes)
        print("\n3. Testing Legacy Endpoints...")
        self.test_endpoint("GET", "/get_roles/", 200, description="Legacy get roles")
        self.test_endpoint("GET", "/get_permissions/", 200, description="Legacy get permissions")
        
        # Test 4: Missing endpoints (should work after our fixes)
        print("\n4. Testing Missing Endpoints...")
        self.test_endpoint("GET", "/ai_metrics/", 200, description="AI metrics")
        self.test_endpoint("GET", "/performance/", 200, description="Performance metrics")
        
        # Test 5: Role management with complex payload
        print("\n5. Testing Role Management with Complex Payload...")
        complex_role_payload = {
            "name": "test_integration_role",
            "label": "Test Integration Role",
            "permissions": [
                {
                    "group": "Users",
                    "count": "2 / 4",
                    "permissions": [
                        {"id": 1, "name": "create_users", "label": "Create Users", "enabled": True},
                        {"id": 2, "name": "view_users", "label": "View Users", "enabled": True}
                    ]
                },
                {
                    "group": "Billing",
                    "count": "1 / 3",
                    "permissions": [
                        {"id": 6, "name": "view_billing", "label": "View Billing", "enabled": True}
                    ]
                }
            ]
        }
        
        self.test_endpoint("POST", "/api/roles/", 200, complex_role_payload, "Create role with complex permissions")
        
        # Test 6: Other core endpoints
        print("\n6. Testing Core Business Endpoints...")
        self.test_endpoint("GET", "/api/properties/", 200, description="Get properties")
        self.test_endpoint("GET", "/api/campaigns/", 200, description="Get campaigns")
        self.test_endpoint("GET", "/api/leads/", 200, description="Get leads")
        
        # Print results
        self.print_results()
        
    def print_results(self):
        """Print comprehensive test results"""
        print("\n" + "=" * 60)
        print("🎯 FRONTEND-BACKEND INTEGRATION TEST RESULTS")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.get("success", False))
        failed_tests = total_tests - passed_tests
        
        print(f"\nTotal Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result.get("success", False):
                    print(f"  • {result['method']} {result['endpoint']} - Status: {result['status_code']} (Expected: {result['expected_status']})")
                    if 'error' in result:
                        print(f"    Error: {result['error']}")
                    elif 'response' in result:
                        print(f"    Response: {str(result['response'])[:100]}...")
        
        print("\n✅ PASSED TESTS:")
        for result in self.test_results:
            if result.get("success", False):
                print(f"  • {result['method']} {result['endpoint']} - {result['description']}")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! Frontend-Backend integration is fully functional!")
        else:
            print(f"\n⚠️  {failed_tests} tests failed. Review and fix issues.")
        
        # Summary of fixes applied
        print("\n" + "=" * 60)
        print("🔧 FIXES APPLIED FOR FRONTEND-BACKEND INTEGRATION")
        print("=" * 60)
        print("1. ✅ Fixed frontend API URLs to use localhost:8140")
        print("2. ✅ Updated RbacAPI to use correct endpoint paths")
        print("3. ✅ Fixed Vite WebSocket configuration")
        print("4. ✅ Added legacy endpoints for frontend compatibility")
        print("5. ✅ Added missing endpoints (ai_metrics, performance)")
        print("6. ✅ Enhanced role management with complex permission structure")
        print("7. ✅ Fixed CORS and connection issues")
        
        print("\n📋 FRONTEND CHANGES MADE:")
        print("• Updated api.js to use localhost:8140 instead of dev.deelflowai.com:8140")
        print("• Fixed RbacAPI endpoints to match backend structure")
        print("• Updated Vite config to use localhost instead of 0.0.0.0")
        
        print("\n📋 BACKEND CHANGES MADE:")
        print("• Added legacy endpoints: /get_roles/, /get_permissions/")
        print("• Added missing endpoints: /ai_metrics/, /performance/")
        print("• Enhanced role management with complex permission structure support")
        print("• Fixed async/sync issues in role service")

if __name__ == "__main__":
    tester = FrontendBackendIntegrationTester()
    tester.run_all_tests()
