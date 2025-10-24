import requests

BASE_URL = "http://localhost:8140"
USERNAME = "arpansarkar@gmail.com"
PASSWORD = "arpan051992"
TIMEOUT = 30

def test_get_property_by_id_retrieve_property_details():
    # Login to get token
    login_url = f"{BASE_URL}/api/auth/login"
    login_payload = {"email": USERNAME, "password": PASSWORD}
    login_resp = requests.post(login_url, json=login_payload, timeout=TIMEOUT)
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    login_data = login_resp.json()
    assert "access_token" in login_data, "access_token missing in login response"
    assert "refresh_token" in login_data, "refresh_token missing in login response"
    access_token = login_data["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    # Create a new property to get its ID for testing
    property_create_url = f"{BASE_URL}/properties/"
    new_property_payload = {
        "address": "123 Test St",
        "city": "Testville",
        "state": "TS",
        "zip": "12345",
        "county": "Test County",
        "property_type": "Single Family",
        "transaction_type": "Sale",
        "description": "A test property for API testing."
    }
    new_property_resp = requests.post(property_create_url, json=new_property_payload, headers=headers, timeout=TIMEOUT)
    assert new_property_resp.status_code == 200, f"Property creation failed: {new_property_resp.text}"
    new_property_data = new_property_resp.json()
    prop_id = new_property_data.get("data", {}).get("id")
    assert isinstance(prop_id, int), "Created property ID not found or invalid"

    try:
        # Test GET /properties/{property_id}/ endpoint
        get_property_url = f"{BASE_URL}/properties/{prop_id}/"
        get_resp = requests.get(get_property_url, headers=headers, timeout=TIMEOUT)
        assert get_resp.status_code == 200, f"GET property by ID failed: {get_resp.text}"
        get_data = get_resp.json()
        assert get_data.get("status") == "success" or get_data.get("status") == "ok" or isinstance(get_data.get("status"), str), "Missing or invalid status field"
        property_info = get_data.get("data")
        assert isinstance(property_info, dict), "Property data should be an object"
        assert property_info.get("id") == prop_id, "Property ID in response does not match requested ID"
        # Optional checks for fields presence
        assert "address" in property_info, "address field missing in property data"
        assert "city" in property_info, "city field missing in property data"
        assert "state" in property_info, "state field missing in property data"
        assert "zip" in property_info, "zip field missing in property data"
        assert "property_type" in property_info, "property_type field missing in property data"
    finally:
        # Clean up: delete the created property
        delete_url = f"{BASE_URL}/properties/{prop_id}/"
        del_resp = requests.delete(delete_url, headers=headers, timeout=TIMEOUT)
        assert del_resp.status_code == 200, f"Property deletion failed: {del_resp.text}"

test_get_property_by_id_retrieve_property_details()