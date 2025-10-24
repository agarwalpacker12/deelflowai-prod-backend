#!/usr/bin/env python3
"""
Test script to verify the campaign creation fix.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8140"

def test_campaign_creation():
    """Test the campaign creation endpoint"""
    print("Testing Campaign Creation Fix")
    print("=" * 50)
    
    # Test payload from the user
    campaign_data = {
        "campaign_type": "buyer_finder",
        "seller_keywords": "",
        "property_year_built_max": "",
        "property_year_built_min": "",
        "seller_parish": "",
        "seller_districts": "",
        "seller_city": "",
        "seller_counties": "",
        "seller_state": "",
        "seller_country": "",
        "buyer_parish": "sdf",
        "buyer_districts": "sdf",
        "buyer_city": "Kolkata",
        "buyer_counties": "sdf",
        "buyer_state": "West Bengal",
        "buyer_country": "",
        "home_ownership_status": "own_home",
        "employment_status": "employed",
        "marital_status": "married",
        "salary_range": "30k_50k",
        "ethnicity": "caucasian",
        "age_range": "26-35",
        "last_qualification": "pre_approved",
        "distress_indicators": [],
        "min_price": 250000,
        "max_price": 750000,
        "minimum_equity": 0,
        "property_type": "",
        "location": "",
        "geographic_scope_type": "ca",
        "use_ai_personalization": True,
        "status": "inactive",
        "email_content": "sdfaf",
        "subject_line": "Test Subject",
        "scheduled_at": "2025-11-06T17:38",
        "budget": 1000,
        "channel": ["email", "direct_mail"],
        "name": "Sourav ",
        "geographic_scope_values": ["West Bengal", "sdf", "Kolkata", "sdf", "sdf"],
        "geographic_scope": {
            "type": "counties",
            "counties": ["Miami-Dade", "Broward", "Palm Beach"]
        }
    }
    
    try:
        print("Sending POST request to /campaigns/")
        response = requests.post(f"{BASE_URL}/campaigns/", json=campaign_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                print("SUCCESS - Campaign created successfully!")
                print(f"Campaign ID: {data.get('data', {}).get('id', 'N/A')}")
                return True
            else:
                print(f"ERROR - API returned error: {data.get('message', 'Unknown error')}")
                return False
        else:
            print(f"ERROR - HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"ERROR - Exception occurred: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting Campaign Creation Test")
    print(f"Testing against: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        if test_campaign_creation():
            print("\n" + "=" * 50)
            print("CAMPAIGN CREATION FIX SUCCESSFUL!")
            print("The db_error issue has been resolved")
        else:
            print("\n" + "=" * 50)
            print("CAMPAIGN CREATION TEST FAILED")
            print("Please check the output above for details")
            
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
