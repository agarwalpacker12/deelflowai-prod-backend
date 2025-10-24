import requests

BASE_URL = "http://localhost:8140"
AUTH_CREDENTIALS = {
    "username": "arpansarkar@gmail.com",
    "password": "arpan051992"
}


def test_tc009_get_stats_dashboard_statistics():
    # Authenticate to get token
    login_url = f"{BASE_URL}/api/auth/login"
    login_payload = {
        "email": AUTH_CREDENTIALS["username"],
        "password": AUTH_CREDENTIALS["password"]
    }
    try:
        login_resp = requests.post(login_url, json=login_payload, timeout=30)
        login_resp.raise_for_status()
    except Exception as e:
        assert False, f"Login failed with error: {e}"

    login_data = login_resp.json()
    # Validate that tokens are at root level
    assert "access_token" in login_data, "access_token not found in login response"
    assert "refresh_token" in login_data, "refresh_token not found in login response"
    access_token = login_data["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    # 1) Verify GET /properties/ includes potential_profit field
    properties_url = f"{BASE_URL}/properties/"
    try:
        resp = requests.get(properties_url, headers=headers, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        assert False, f"GET /properties/ failed with error: {e}"

    resp_json = resp.json()
    assert resp.status_code == 200, f"Expected 200 but got {resp.status_code} for GET /properties/"
    assert isinstance(resp_json, dict), "/properties/ response is not a dict"
    assert "data" in resp_json, "/properties/ response missing 'data' field"
    assert isinstance(resp_json["data"], list), "'data' field in /properties/ is not a list"
    if len(resp_json["data"]) > 0:
        first_property = resp_json["data"][0]
        assert "potential_profit" in first_property, "'potential_profit' field not found in property item"

    # 2) Verify PUT /properties/{id}/ and then get to confirm update

    # Create a property to update
    new_property_payload = {
        "address": "123 Test St",
        "city": "Testville",
        "state": "TS",
        "zip": "12345",
        "county": "Test County",
        "property_type": "Residential",
        "transaction_type": "Sale",
        "description": "Test description"
    }
    try:
        create_resp = requests.post(properties_url, headers=headers, json=new_property_payload, timeout=30)
        create_resp.raise_for_status()
    except Exception as e:
        assert False, f"POST /properties/ creation failed with error: {e}"

    create_json = create_resp.json()
    property_id = create_json.get("data", {}).get("id")
    assert property_id is not None, "Failed to create a property for update test"

    updated_address = "456 Updated Ave"
    updated_city = "Update City"
    updated_state = "UP"

    update_url = f"{BASE_URL}/properties/{property_id}/"
    update_payload = {
        "address": updated_address,
        "city": updated_city,
        "state": updated_state
    }
    try:
        update_resp = requests.put(update_url, headers=headers, json=update_payload, timeout=30)
        update_resp.raise_for_status()
    except Exception as e:
        # Clean up created property before failing
        requests.delete(update_url, headers=headers, timeout=30)
        assert False, f"PUT /properties/{property_id}/ failed with error: {e}"

    assert update_resp.status_code == 200, f"PUT update did not return 200 but {update_resp.status_code}"

    # Retrieve property to confirm update
    try:
        get_resp = requests.get(update_url, headers=headers, timeout=30)
        get_resp.raise_for_status()
    except Exception as e:
        # Clean up created property before failing
        requests.delete(update_url, headers=headers, timeout=30)
        assert False, f"GET /properties/{property_id}/ failed after update with error: {e}"

    prop_data = get_resp.json().get("data")
    assert prop_data is not None, "Property data missing after update"
    assert prop_data.get("address") == updated_address, "Address not updated correctly"
    assert prop_data.get("city") == updated_city, "City not updated correctly"
    assert prop_data.get("state") == updated_state, "State not updated correctly"

    # 3) Verify POST /api/auth/login returns tokens at root level: already validated above.

    # 4) Test the GET /stats dashboard endpoint that was previously 405

    stats_url = f"{BASE_URL}/stats"
    try:
        stats_resp = requests.get(stats_url, headers=headers, timeout=30)
        stats_resp.raise_for_status()
    except Exception as e:
        # Clean up created property before failing
        requests.delete(update_url, headers=headers, timeout=30)
        assert False, f"GET /stats failed with error: {e}"

    assert stats_resp.status_code == 200, f"Expected 200 but got {stats_resp.status_code} for GET /stats"

    stats_json = stats_resp.json()
    assert "data" in stats_json, "/stats response missing 'data' field"
    stats_data = stats_json["data"]
    expected_fields = {"total_revenue", "active_users", "properties_listed", "total_deals"}
    missing_fields = expected_fields - stats_data.keys()
    assert not missing_fields, f"/stats response missing fields: {missing_fields}"

    # Cleanup created property
    try:
        del_resp = requests.delete(update_url, headers=headers, timeout=30)
        del_resp.raise_for_status()
    except Exception as e:
        assert False, f"Cleanup failed for property {property_id} with error: {e}"


test_tc009_get_stats_dashboard_statistics()