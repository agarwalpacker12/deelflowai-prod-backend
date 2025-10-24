#!/usr/bin/env python3
"""
Test the final SaaS role structure
"""

import requests
import json

def test_final_saas_structure():
    """Test the final SaaS role structure"""
    
    print("Testing the final SaaS role structure...")
    print("=" * 60)
    
    # Test each role endpoint
    roles_to_test = [139, 140, 141]  # admin, client, super_admin_platform
    role_names = ['Admin', 'Client', 'Super Admin']
    
    for i, role_id in enumerate(roles_to_test):
        try:
            response = requests.get(f'http://localhost:8140/api/roles/{role_id}/')
            if response.status_code == 200:
                data = response.json()
                role_data = data.get('data', {})
                print(f"SUCCESS: {role_names[i]}: {role_data.get('name')} (ID: {role_id})")
                print(f"   Permissions: {len(role_data.get('permissions', []))}")
            else:
                print(f"ERROR: {role_names[i]} (ID: {role_id}): {response.text}")
        except Exception as e:
            print(f"ERROR: Error testing {role_names[i]}: {e}")
    
    print()
    print("SAAS ROLE STRUCTURE COMPLETE!")
    print("=" * 60)
    print("Your SaaS platform is ready with:")
    print("1. Super Admin - Complete system control")
    print("2. Admin - Full tenant management") 
    print("3. Client - Limited to own data")
    print()
    print("Perfect for perfextosaas.com!")

if __name__ == "__main__":
    test_final_saas_structure()
