import requests

BASE_URL = "http://localhost:8140"
AUTH_CREDENTIALS = {
    "username": "arpansarkar@gmail.com",
    "password": "arpan051992"
}
TIMEOUT = 30

def test_tc004_put_properties_property_id_update_property():
    # 1. User Login to get access token
    login_url = f"{BASE_URL}/api/auth/login"
    login_payload = {
        "email": AUTH_CREDENTIALS["username"],
        "password": AUTH_CREDENTIALS["password"]
    }
    try:
        login_resp = requests.post(login_url, json=login_payload, timeout=TIMEOUT)
        assert login_resp.status_code == 200, f"Login failed with status {login_resp.status_code}"
        login_data = login_resp.json()
        # The tokens are at root level
        access_token = login_data.get("access_token")
        refresh_token = login_data.get("refresh_token")
        assert access_token and refresh_token, "Access or refresh token missing in login response"
    except Exception as e:
        raise AssertionError(f"Login API call failed: {e}")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 2. Create a property to update (since no property_id provided)
    create_url = f"{BASE_URL}/properties/"
    create_payload = {
        "address": "123 Original St",
        "city": "Oldtown",
        "state": "OS",
        "zip": "12345",
        "county": "Oldcounty",
        "property_type": "Single Family",
        "transaction_type": "Sale",
        "description": "Original property description"
    }
    property_id = None
    try:
        create_resp = requests.post(create_url, json=create_payload, headers=headers, timeout=TIMEOUT)
        assert create_resp.status_code == 200, f"Property creation failed with status {create_resp.status_code}"
        create_data = create_resp.json()
        property_id = create_data.get("data", {}).get("id")
        assert property_id is not None, "Created property ID is missing"
        
        # 3. Update property details with PUT /properties/{property_id}/
        update_url = f"{BASE_URL}/properties/{property_id}/"
        update_payload = {
            "address": "456 Updated Ave",
            "city": "Newcity",
            "state": "NS"
        }
        update_resp = requests.put(update_url, json=update_payload, headers=headers, timeout=TIMEOUT)
        assert update_resp.status_code == 200, f"Property update failed with status {update_resp.status_code}"

        # 4. Retrieve the updated property with GET /properties/{property_id}/ to verify changes
        get_url = update_url
        get_resp = requests.get(get_url, headers=headers, timeout=TIMEOUT)
        assert get_resp.status_code == 200, f"Get property failed with status {get_resp.status_code}"
        get_data = get_resp.json()
        updated_property = get_data.get("data", {})
        assert updated_property.get("address") == update_payload["address"], "Address was not updated correctly"
        assert updated_property.get("city") == update_payload["city"], "City was not updated correctly"
        assert updated_property.get("state") == update_payload["state"], "State was not updated correctly"

        # 5. Test GET /properties/ to check if potential_profit field exists in the property list
        list_url = f"{BASE_URL}/properties/"
        list_resp = requests.get(list_url, headers=headers, timeout=TIMEOUT)
        assert list_resp.status_code == 200, f"Property list failed with status {list_resp.status_code}"
        list_data = list_resp.json()
        properties = list_data.get("data", [])
        # Find our property in the list:
        found_prop = None
        for prop in properties:
            if prop.get("id") == property_id:
                found_prop = prop
                break
        assert found_prop is not None, "Updated property not found in property list"
        assert "potential_profit" in found_prop, "'potential_profit' field missing in property list"

        # 6. Test dashboard endpoints that previously showed 405 to confirm 200 responses

        # GET /stats
        stats_url = f"{BASE_URL}/stats"
        stats_resp = requests.get(stats_url, headers=headers, timeout=TIMEOUT)
        assert stats_resp.status_code == 200, f"Dashboard stats failed with status {stats_resp.status_code}"
        stats_data = stats_resp.json()
        assert "data" in stats_data, "Dashboard stats response missing data field"

        # GET /total-revenue/
        revenue_url = f"{BASE_URL}/total-revenue/"
        revenue_resp = requests.get(revenue_url, headers=headers, timeout=TIMEOUT)
        assert revenue_resp.status_code == 200, f"Total revenue failed with status {revenue_resp.status_code}"
        revenue_data = revenue_resp.json()
        assert "data" in revenue_data, "Total revenue response missing data field"

    finally:
        # Clean up: Delete the created property if it exists
        if property_id is not None:
            delete_url = f"{BASE_URL}/properties/{property_id}/"
            try:
                del_resp = requests.delete(delete_url, headers=headers, timeout=TIMEOUT)
                assert del_resp.status_code == 200, f"Failed to delete property with id {property_id}"
            except Exception as e:
                raise AssertionError(f"Cleanup delete property failed: {e}")

test_tc004_put_properties_property_id_update_property()