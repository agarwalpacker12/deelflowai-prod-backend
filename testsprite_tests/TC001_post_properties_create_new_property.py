import requests

base_url = "http://localhost:8140"
login_url = f"{base_url}/api/auth/login"
properties_url = f"{base_url}/properties/"

credentials = {
    "email": "arpansarkar@gmail.com",
    "password": "arpan051992"
}

def test_post_properties_create_new_property():
    # Authenticate first to get token
    try:
        login_response = requests.post(login_url, json=credentials, timeout=30)
        assert login_response.status_code == 200, f"Login failed with status {login_response.status_code}"
        login_data = login_response.json()
        assert "access_token" in login_data, "access_token not in login response"
        token = login_data["access_token"]
    except Exception as e:
        raise AssertionError(f"Authentication failed: {e}")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Prepare payload with all required fields plus some optional
    payload = {
        "address": "123 Test Ave",
        "city": "Testville",
        "state": "TS",
        "zip": "12345",
        "county": "Test County",
        "property_type": "Single Family",
        "transaction_type": "Sale",
        "description": "Test property for automation",
        "unit": "1A",
        "bedrooms": 3,
        "bathrooms": 2.5,
        "square_feet": 1800,
        "lot_size": 0.25,
        "year_built": 1995,
        "purchase_price": 250000,
        "arv": 300000,
        "repair_estimate": 15000,
        "holding_costs": 5000,
        "assignment_fee": 8000,
        "seller_notes": "Motivated seller, quick close possible"
    }

    prop_id = None

    try:
        # Create property
        response = requests.post(properties_url, json=payload, headers=headers, timeout=30)
        assert response.status_code == 200, f"Property creation failed with status {response.status_code}"

        json_data = response.json()
        assert json_data.get("status") == "success", "Response status not success"
        data = json_data.get("data")
        assert data is not None, "Response data missing"
        prop_id = data.get("id")
        assert isinstance(prop_id, int), "Property ID is missing or not integer"
        assert data.get("address") == payload["address"], "Address in response does not match"

        potential_profit = data.get("potential_profit")
        assert potential_profit is not None, "potential_profit field missing in response"
        assert isinstance(potential_profit, (int, float)), "potential_profit is not a number"
        # Optionally check potential_profit calculation is reasonable (arv - purchase_price - repair_estimate - holding_costs - assignment_fee)
        expected_profit = (
            payload["arv"]
            - payload["purchase_price"]
            - payload["repair_estimate"]
            - payload["holding_costs"]
            - payload["assignment_fee"]
        )
        # Allow a small delta for floating point
        assert abs(potential_profit - expected_profit) < 1e-2, f"potential_profit incorrect: expected {expected_profit}, got {potential_profit}"

    finally:
        # Cleanup: delete the created property
        if prop_id is not None:
            try:
                delete_response = requests.delete(f"{properties_url}{prop_id}/", headers=headers, timeout=30)
                assert delete_response.status_code == 200, f"Failed to delete property with id {prop_id}"
            except Exception:
                pass  # Ignore cleanup errors

test_post_properties_create_new_property()
