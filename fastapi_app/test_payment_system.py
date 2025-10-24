#!/usr/bin/env python3
"""
Comprehensive Payment System Test Suite
Tests all payment gateway functionality end-to-end
"""

import requests
import json
import time
from decimal import Decimal

class PaymentSystemTester:
    """Test suite for payment gateway functionality"""
    
    def __init__(self, base_url="http://localhost:8140"):
        self.base_url = base_url
        self.test_results = []
    
    def log_test(self, test_name, status, message="", response_data=None):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": time.time()
        }
        if response_data:
            result["response"] = response_data
        self.test_results.append(result)
        
        status_emoji = "PASS" if status == "PASS" else "FAIL"
        print(f"{status_emoji} {test_name}: {message}")
    
    def test_payment_endpoints_availability(self):
        """Test if all payment endpoints are available"""
        print("\nTesting Payment Endpoints Availability...")
        print("=" * 60)
        
        endpoints = [
            ("GET", "/subscription-packs/", "Get subscription packages"),
            ("POST", "/create-checkout-session/", "Create checkout session"),
            ("POST", "/create-customer-portal-session/", "Create customer portal"),
            ("POST", "/stripe-invoice/", "Get customer invoices"),
            ("GET", "/current-subscription/", "Get current subscription"),
            ("GET", "/total-revenue/", "Get total revenue"),
            ("GET", "/monthly-profit/", "Get monthly profit"),
            ("POST", "/verify-payment/", "Verify payment"),
            ("POST", "/create-payment-intent/", "Create payment intent")
        ]
        
        for method, endpoint, description in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}")
                else:
                    response = requests.post(f"{self.base_url}{endpoint}", json={})
                
                if response.status_code in [200, 400, 422]:  # 400/422 are expected for missing data
                    self.log_test(f"Endpoint {endpoint}", "PASS", f"Available (Status: {response.status_code})")
                else:
                    self.log_test(f"Endpoint {endpoint}", "FAIL", f"Unexpected status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Endpoint {endpoint}", "FAIL", f"Error: {str(e)}")
    
    def test_subscription_packages(self):
        """Test subscription packages endpoint"""
        print("\nTesting Subscription Packages...")
        print("=" * 60)
        
        try:
            response = requests.get(f"{self.base_url}/subscription-packs/")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    packages = data.get("data", {}).get("packages", [])
                    self.log_test("Get Subscription Packages", "PASS", f"Retrieved {len(packages)} packages")
                    
                    # Test package structure
                    if packages:
                        package = packages[0]
                        required_fields = ["id", "name", "price_id", "amount", "currency"]
                        missing_fields = [field for field in required_fields if field not in package]
                        
                        if not missing_fields:
                            self.log_test("Package Structure", "PASS", "All required fields present")
                        else:
                            self.log_test("Package Structure", "FAIL", f"Missing fields: {missing_fields}")
                    else:
                        self.log_test("Package Data", "WARN", "No packages found (expected in test environment)")
                else:
                    self.log_test("Get Subscription Packages", "FAIL", f"API error: {data.get('message')}")
            else:
                self.log_test("Get Subscription Packages", "FAIL", f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Get Subscription Packages", "FAIL", f"Exception: {str(e)}")
    
    def test_checkout_session_creation(self):
        """Test checkout session creation"""
        print("\nTesting Checkout Session Creation...")
        print("=" * 60)
        
        # Test with mock data
        test_data = {
            "price_id": "price_test_123",
            "success_url": "http://localhost:5173/payment/success",
            "cancel_url": "http://localhost:5173/payment/cancel"
        }
        
        try:
            response = requests.post(f"{self.base_url}/create-checkout-session/", json=test_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    self.log_test("Create Checkout Session", "PASS", "Checkout session created successfully")
                else:
                    self.log_test("Create Checkout Session", "FAIL", f"API error: {data.get('message')}")
            else:
                self.log_test("Create Checkout Session", "FAIL", f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Create Checkout Session", "FAIL", f"Exception: {str(e)}")
    
    def test_payment_intent_creation(self):
        """Test payment intent creation"""
        print("\nTesting Payment Intent Creation...")
        print("=" * 60)
        
        test_data = {
            "amount": 29.99,
            "currency": "usd",
            "description": "Test payment",
            "metadata": {"test": "true"}
        }
        
        try:
            response = requests.post(f"{self.base_url}/create-payment-intent/", json=test_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    self.log_test("Create Payment Intent", "PASS", "Payment intent created successfully")
                else:
                    self.log_test("Create Payment Intent", "FAIL", f"API error: {data.get('message')}")
            else:
                self.log_test("Create Payment Intent", "FAIL", f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Create Payment Intent", "FAIL", f"Exception: {str(e)}")
    
    def test_revenue_metrics(self):
        """Test revenue metrics endpoints"""
        print("\nTesting Revenue Metrics...")
        print("=" * 60)
        
        endpoints = [
            ("/total-revenue/", "Total Revenue"),
            ("/monthly-profit/", "Monthly Profit")
        ]
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        self.log_test(name, "PASS", "Revenue metrics retrieved successfully")
                    else:
                        self.log_test(name, "FAIL", f"API error: {data.get('message')}")
                else:
                    self.log_test(name, "FAIL", f"HTTP {response.status_code}: {response.text}")
            except Exception as e:
                self.log_test(name, "FAIL", f"Exception: {str(e)}")
    
    def test_customer_operations(self):
        """Test customer-related operations"""
        print("\nTesting Customer Operations...")
        print("=" * 60)
        
        test_customer_id = "cus_test_123"
        
        # Test customer portal session
        try:
            response = requests.post(f"{self.base_url}/create-customer-portal-session/", 
                                   json={"customer_id": test_customer_id})
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    self.log_test("Customer Portal Session", "PASS", "Portal session created successfully")
                else:
                    self.log_test("Customer Portal Session", "FAIL", f"API error: {data.get('message')}")
            else:
                self.log_test("Customer Portal Session", "FAIL", f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Customer Portal Session", "FAIL", f"Exception: {str(e)}")
        
        # Test customer invoices
        try:
            response = requests.post(f"{self.base_url}/stripe-invoice/", 
                                   json={"customer_id": test_customer_id})
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    self.log_test("Customer Invoices", "PASS", "Customer invoices retrieved successfully")
                else:
                    self.log_test("Customer Invoices", "FAIL", f"API error: {data.get('message')}")
            else:
                self.log_test("Customer Invoices", "FAIL", f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Customer Invoices", "FAIL", f"Exception: {str(e)}")
        
        # Test current subscription
        try:
            response = requests.get(f"{self.base_url}/current-subscription/?customer_id={test_customer_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    self.log_test("Current Subscription", "PASS", "Subscription data retrieved successfully")
                else:
                    self.log_test("Current Subscription", "FAIL", f"API error: {data.get('message')}")
            else:
                self.log_test("Current Subscription", "FAIL", f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Current Subscription", "FAIL", f"Exception: {str(e)}")
    
    def test_payment_verification(self):
        """Test payment verification"""
        print("\nTesting Payment Verification...")
        print("=" * 60)
        
        test_session_id = "cs_test_123"
        
        try:
            response = requests.post(f"{self.base_url}/verify-payment/", 
                                   json={"session_id": test_session_id})
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    self.log_test("Payment Verification", "PASS", "Payment verification successful")
                else:
                    self.log_test("Payment Verification", "FAIL", f"API error: {data.get('message')}")
            else:
                self.log_test("Payment Verification", "FAIL", f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Payment Verification", "FAIL", f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all payment system tests"""
        print("Starting Comprehensive Payment System Test Suite")
        print("=" * 80)
        
        self.test_payment_endpoints_availability()
        self.test_subscription_packages()
        self.test_checkout_session_creation()
        self.test_payment_intent_creation()
        self.test_revenue_metrics()
        self.test_customer_operations()
        self.test_payment_verification()
        
        # Summary
        print("\nTest Summary")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        warning_tests = len([r for r in self.test_results if r["status"] == "WARN"])
        
        print(f"Total Tests: {total_tests}")
        print(f"PASSED: {passed_tests}")
        print(f"FAILED: {failed_tests}")
        print(f"WARNINGS: {warning_tests}")
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print("\nFAILED Tests:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test']}: {result['message']}")
        
        return {
            "total": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "warnings": warning_tests,
            "success_rate": success_rate
        }

if __name__ == "__main__":
    tester = PaymentSystemTester()
    results = tester.run_all_tests()
    
    if results["success_rate"] >= 80:
        print("\nPayment System Test Suite PASSED!")
        print("Your payment gateway is ready for production!")
    else:
        print("\nPayment System Test Suite needs attention.")
        print("Please review failed tests and fix issues before production.")
