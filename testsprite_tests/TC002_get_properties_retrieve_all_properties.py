import requests

BASE_URL = "http://localhost:8140"
AUTH_CREDENTIALS = {
    "username": "arpansarkar@gmail.com",
    "password": "arpan051992"
}
TIMEOUT = 30

def get_basic_auth_token():
    # For this test, use POST /api/auth/login to get access token via email/password
    login_url = f"{BASE_URL}/api/auth/login"
    login_payload = {
        "email": AUTH_CREDENTIALS["username"],
        "password": AUTH_CREDENTIALS["password"]
    }
    try:
        resp = requests.post(login_url, json=login_payload, timeout=TIMEOUT)
        resp.raise_for_status()
        token_data = resp.json()
        assert "access_token" in token_data, "access_token missing in login response"
        assert "refresh_token" in token_data, "refresh_token missing in login response"
        return token_data["access_token"]
    except Exception as e:
        raise RuntimeError(f"Failed to get auth token: {e}")

def test_get_properties_retrieve_all_properties():
    access_token = get_basic_auth_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    url = f"{BASE_URL}/properties/"

    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
    except Exception as e:
        raise RuntimeError(f"GET /properties/ request failed: {e}")

    try:
        response.raise_for_status()
    except Exception as e:
        raise AssertionError(f"GET /properties/ returned error status code {response.status_code}: {e}")

    try:
        resp_json = response.json()
    except Exception as e:
        raise AssertionError(f"Response is not valid JSON: {e}")

    # Validate top-level keys
    assert isinstance(resp_json, dict), "Response JSON is not an object"
    assert "status" in resp_json, "'status' field missing in response"
    assert "data" in resp_json, "'data' field missing in response"
    assert resp_json["status"] == "success" or resp_json["status"] == "ok", "Unexpected status value"

    data = resp_json["data"]
    assert isinstance(data, list), "'data' field is not a list"

    # Check at least one property or just verify all fields if list empty
    for prop in data:
        assert isinstance(prop, dict), "Property entry is not an object"
        # Required fields according to schema
        expected_fields = [
            "id",
            "address",
            "city",
            "state",
            "zip",
            "property_type",
            "bedrooms",
            "bathrooms",
            "square_feet",
            "purchase_price",
            "arv",
            "potential_profit"
        ]
        for field in expected_fields:
            assert field in prop, f"Field '{field}' missing in property"
        # Validate types
        assert isinstance(prop["id"], int), "'id' should be int"
        assert isinstance(prop["address"], str), "'address' should be str"
        assert isinstance(prop["city"], str), "'city' should be str"
        assert isinstance(prop["state"], str), "'state' should be str"
        assert isinstance(prop["zip"], str), "'zip' should be str"
        assert isinstance(prop["property_type"], str), "'property_type' should be str"
        assert isinstance(prop["bedrooms"], int), "'bedrooms' should be int"
        assert isinstance(prop["bathrooms"], (int, float)), "'bathrooms' should be number"
        assert isinstance(prop["square_feet"], int), "'square_feet' should be int"
        assert isinstance(prop["purchase_price"], (int, float)), "'purchase_price' should be number"
        assert isinstance(prop["arv"], (int, float)), "'arv' should be number"
        # potential_profit must be a number (int or float)
        assert isinstance(prop["potential_profit"], (int, float)), "'potential_profit' should be number"

test_get_properties_retrieve_all_properties()