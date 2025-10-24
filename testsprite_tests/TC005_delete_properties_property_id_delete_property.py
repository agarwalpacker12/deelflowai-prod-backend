import requests

BASE_URL = "http://localhost:8140"
AUTH_CREDENTIALS = {
    "username": "arpansarkar@gmail.com",
    "password": "arpan051992"
}


def get_auth_token():
    login_url = f"{BASE_URL}/api/auth/login"
    login_payload = {
        "email": AUTH_CREDENTIALS["username"],
        "password": AUTH_CREDENTIALS["password"]
    }
    try:
        response = requests.post(login_url, json=login_payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        access_token = data.get("access_token")
        refresh_token = data.get("refresh_token")
        assert access_token, "access_token not found in login response"
        assert refresh_token, "refresh_token not found in login response"
        return access_token
    except Exception as e:
        raise RuntimeError(f"Authentication failed: {e}")


def create_property(headers):
    url = f"{BASE_URL}/properties/"
    payload = {
        "address": "1234 Delete Test St",
        "city": "Testville",
        "state": "TS",
        "zip": "12345",
        "county": "Test County",
        "property_type": "Single Family",
        "transaction_type": "Sale",
        "description": "Property created for delete test",
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        resp_json = response.json()
        property_id = resp_json.get("data", {}).get("id")
        assert property_id is not None, "Property ID not returned after creation"
        return property_id
    except Exception as e:
        raise RuntimeError(f"Property creation failed: {e}")


def delete_property_test():
    token = get_auth_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    property_id = None
    try:
        # Create property so we have a property to delete
        property_id = create_property(headers)

        # DELETE /properties/{property_id}/ endpoint
        delete_url = f"{BASE_URL}/properties/{property_id}/"
        delete_resp = requests.delete(delete_url, headers=headers, timeout=30)
        assert delete_resp.status_code == 200, f"Expected status code 200 but got {delete_resp.status_code}"

        # Optionally verify the property no longer exists by GET; should return 404 or not found status
        get_url = f"{BASE_URL}/properties/{property_id}/"
        get_resp = requests.get(get_url, headers=headers, timeout=30)
        assert get_resp.status_code == 404 or get_resp.status_code == 400, "Deleted property still accessible"

        # Additional checks: Verify GET /properties/ includes 'potential_profit' field in list items
        list_url = f"{BASE_URL}/properties/"
        list_resp = requests.get(list_url, headers=headers, timeout=30)
        assert list_resp.status_code == 200, f"Failed to get properties list, status {list_resp.status_code}"
        list_data = list_resp.json().get("data", [])
        if list_data:
            sample_property = list_data[0]
            assert "potential_profit" in sample_property, "'potential_profit' field not found in properties list"

        # Additional: Test the PUT /properties/{id}/ endpoint update and confirm update
        # Create a property for update test
        up_property_id = create_property(headers)
        try:
            update_url = f"{BASE_URL}/properties/{up_property_id}/"
            update_payload = {
                "address": "Updated Address",
                "city": "Updated City",
                "state": "UP"
            }
            put_resp = requests.put(update_url, json=update_payload, headers=headers, timeout=30)
            assert put_resp.status_code == 200, f"PUT update failed with status {put_resp.status_code}"

            get_after_update_resp = requests.get(update_url, headers=headers, timeout=30)
            assert get_after_update_resp.status_code == 200, f"GET after update failed with status {get_after_update_resp.status_code}"
            get_data = get_after_update_resp.json().get("data", {})
            assert get_data.get("address") == update_payload["address"], "Address not updated correctly"
            assert get_data.get("city") == update_payload["city"], "City not updated correctly"
            assert get_data.get("state") == update_payload["state"], "State not updated correctly"
        finally:
            # Clean up update test property
            requests.delete(f"{BASE_URL}/properties/{up_property_id}/", headers=headers, timeout=30)

        # Additional: Test User Login endpoint returns access_token and refresh_token at root
        login_url = f"{BASE_URL}/api/auth/login"
        login_payload = {
            "email": AUTH_CREDENTIALS["username"],
            "password": AUTH_CREDENTIALS["password"]
        }
        login_resp = requests.post(login_url, json=login_payload, timeout=30)
        assert login_resp.status_code == 200, f"Login failed with status {login_resp.status_code}"
        login_json = login_resp.json()
        assert "access_token" in login_json, "'access_token' not found in login response"
        assert "refresh_token" in login_json, "'refresh_token' not found in login response"

        # Additional: Test dashboard endpoints to ensure no 405 error and status 200

        dashboard_endpoints = [
            "/stats",
            "/total-revenue/"
        ]

        for endpoint in dashboard_endpoints:
            url = f"{BASE_URL}{endpoint}"
            resp = requests.get(url, headers=headers, timeout=30)
            assert resp.status_code == 200, f"Dashboard endpoint {endpoint} returned status {resp.status_code}"
    finally:
        if property_id is not None:
            # Cleanup property created for delete test if it still exists
            requests.delete(f"{BASE_URL}/properties/{property_id}/", headers=headers, timeout=30)


delete_property_test()