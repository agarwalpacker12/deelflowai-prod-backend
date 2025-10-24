import requests

BASE_URL = "http://localhost:8140"
TIMEOUT = 30
LOGIN_ENDPOINT = "/api/auth/login"
PROPERTIES_ENDPOINT = "/properties/"
DASHBOARD_STATS_ENDPOINT = "/stats"
TOTAL_REVENUE_ENDPOINT = "/total-revenue/"

USERNAME = "arpansarkar@gmail.com"
PASSWORD = "arpan051992"


def test_post_api_auth_login_user_login():
    # Test User Login Endpoint
    login_url = BASE_URL + LOGIN_ENDPOINT
    login_payload = {
        "email": USERNAME,
        "password": PASSWORD
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        login_response = requests.post(login_url, json=login_payload, headers=headers, timeout=TIMEOUT)
        assert login_response.status_code == 200, f"Expected 200 but got {login_response.status_code}"

        login_json = login_response.json()
        # The access_token and refresh_token should be at root level of the response JSON
        assert "access_token" in login_json, "access_token missing in login response"
        assert "refresh_token" in login_json, "refresh_token missing in login response"

        access_token = login_json["access_token"]
        refresh_token = login_json["refresh_token"]
        token_type = login_json.get("token_type", "")
        assert isinstance(access_token, str) and access_token, "Invalid access_token"
        assert isinstance(refresh_token, str) and refresh_token, "Invalid refresh_token"
        assert isinstance(token_type, str) and token_type, "Invalid token_type"

    except requests.RequestException as e:
        assert False, f"RequestException during login: {str(e)}"

    # Test GET /properties/ and ensure it includes potential_profit field
    properties_url = BASE_URL + PROPERTIES_ENDPOINT
    try:
        props_response = requests.get(properties_url, timeout=TIMEOUT)
        assert props_response.status_code == 200, f"Expected 200 but got {props_response.status_code}"
        props_json = props_response.json()
        assert "data" in props_json and isinstance(props_json["data"], list), "Invalid properties data structure"
        if len(props_json["data"]) > 0:
            # Check that 'potential_profit' field exists in at least one property item
            assert "potential_profit" in props_json["data"][0], "'potential_profit' field missing in property item"
    except requests.RequestException as e:
        assert False, f"RequestException during GET properties: {str(e)}"

    # Test PUT /properties/{id}/ updates property and GET reflects update
    # Create a new property first to update
    create_payload = {
        "address": "123 Test St",
        "city": "Testville",
        "state": "TS",
        "zip": "12345",
        "county": "Test County",
        "property_type": "Single Family",
        "transaction_type": "Sale",
        "description": "Test property for update"
    }
    property_id = None
    try:
        create_resp = requests.post(properties_url, json=create_payload, timeout=TIMEOUT)
        assert create_resp.status_code == 200, f"Property creation failed with status {create_resp.status_code}"
        create_json = create_resp.json()
        assert "data" in create_json and "id" in create_json["data"], "Property creation response missing id"
        property_id = create_json["data"]["id"]

        # Update property
        update_payload = {
            "address": "456 Updated Ave",
            "city": "Update City",
            "state": "UP"
        }
        update_url = f"{properties_url}{property_id}/"
        update_resp = requests.put(update_url, json=update_payload, timeout=TIMEOUT)
        assert update_resp.status_code == 200, f"Property update failed with status {update_resp.status_code}"

        # GET property and verify updates
        get_resp = requests.get(update_url, timeout=TIMEOUT)
        assert get_resp.status_code == 200, f"Property get after update failed with status {get_resp.status_code}"
        get_json = get_resp.json()
        data = get_json.get("data", {})
        assert data.get("address") == update_payload["address"], "Address did not update correctly"
        assert data.get("city") == update_payload["city"], "City did not update correctly"
        assert data.get("state") == update_payload["state"], "State did not update correctly"

    except requests.RequestException as e:
        assert False, f"RequestException during property create/update/get: {str(e)}"
    finally:
        # Cleanup: delete created property if exists
        if property_id:
            try:
                del_resp = requests.delete(f"{properties_url}{property_id}/", timeout=TIMEOUT)
                assert del_resp.status_code == 200, f"Failed to delete property with id {property_id}"
            except requests.RequestException as e:
                # Log deletion failed but do not fail test due to cleanup
                pass

    # Test dashboard endpoints that were showing 405 errors to ensure they still work
    try:
        stats_url = BASE_URL + DASHBOARD_STATS_ENDPOINT
        stats_resp = requests.get(stats_url, timeout=TIMEOUT)
        assert stats_resp.status_code == 200, f"Dashboard /stats endpoint failed with {stats_resp.status_code}"
        stats_json = stats_resp.json()
        assert "data" in stats_json, "No data in /stats response"

        total_revenue_url = BASE_URL + TOTAL_REVENUE_ENDPOINT
        revenue_resp = requests.get(total_revenue_url, timeout=TIMEOUT)
        assert revenue_resp.status_code == 200, f"Dashboard /total-revenue/ endpoint failed with {revenue_resp.status_code}"
        revenue_json = revenue_resp.json()
        assert "data" in revenue_json, "No data in /total-revenue/ response"

    except requests.RequestException as e:
        assert False, f"RequestException during dashboard endpoint tests: {str(e)}"


test_post_api_auth_login_user_login()