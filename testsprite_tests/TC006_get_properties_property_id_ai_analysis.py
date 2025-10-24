import requests

BASE_URL = "http://localhost:8140"
USERNAME = "arpansarkar@gmail.com"
PASSWORD = "arpan051992"
TIMEOUT = 30


def test_get_properties_property_id_ai_analysis():
    # Login to get token
    login_url = f"{BASE_URL}/api/auth/login"
    login_payload = {
        "email": USERNAME,
        "password": PASSWORD
    }
    try:
        login_resp = requests.post(login_url, json=login_payload, timeout=TIMEOUT)
        login_resp.raise_for_status()
    except Exception as e:
        assert False, f"Login request failed: {e}"
    login_data = login_resp.json()
    assert "access_token" in login_data and "refresh_token" in login_data, "Tokens not found in login response"

    access_token = login_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Create a property to test AI analysis endpoint
    create_url = f"{BASE_URL}/properties/"
    new_property_payload = {
        "address": "123 AI Tester St",
        "city": "Testville",
        "state": "TS",
        "zip": "12345",
        "county": "Test County",
        "property_type": "Single Family",
        "transaction_type": "Sale",
        "description": "Property created for AI analysis test"
    }
    prop_id = None

    try:
        create_resp = requests.post(create_url, json=new_property_payload, headers=headers, timeout=TIMEOUT)
        create_resp.raise_for_status()
        create_data = create_resp.json()
        assert create_data.get("status") == "success" or create_data.get("status") == "ok" or "data" in create_data, "Unexpected create response status"
        prop_id = create_data.get("data", {}).get("id")
        assert isinstance(prop_id, int), "Property ID not found or invalid in create response"

        # Call GET /properties/{property_id}/ai-analysis/
        ai_analysis_url = f"{BASE_URL}/properties/{prop_id}/ai-analysis/"
        ai_resp = requests.get(ai_analysis_url, headers=headers, timeout=TIMEOUT)
        ai_resp.raise_for_status()

        ai_data = ai_resp.json()
        assert ai_data.get("status") == "success" or ai_data.get("status") == "ok", "AI analysis status not success"

        data = ai_data.get("data")
        assert data is not None and isinstance(data, dict), "AI analysis data missing or invalid"

        # Check required fields in the AI analysis data
        expected_fields = ["analysis_type", "confidence_score", "recommended_price", "market_analysis", "risk_assessment", "recommendations"]
        for field in expected_fields:
            assert field in data, f"Field '{field}' missing in AI analysis data"

        # Validate field types
        assert isinstance(data["analysis_type"], str), "analysis_type should be string"
        assert isinstance(data["confidence_score"], (float, int)), "confidence_score should be numeric"
        assert isinstance(data["recommended_price"], (float, int)), "recommended_price should be numeric"
        assert isinstance(data["market_analysis"], dict), "market_analysis should be object"
        assert isinstance(data["risk_assessment"], dict), "risk_assessment should be object"
        assert isinstance(data["recommendations"], list), "recommendations should be a list"
        for rec in data["recommendations"]:
            assert isinstance(rec, str), "each recommendation should be string"

    finally:
        # Cleanup - delete the created property
        if prop_id is not None:
            try:
                del_url = f"{BASE_URL}/properties/{prop_id}/"
                del_resp = requests.delete(del_url, headers=headers, timeout=TIMEOUT)
                del_resp.raise_for_status()
                del_data = del_resp.json()
                assert del_data.get("status") == "success" or del_data.get("status") == "ok", "Delete property status not success"
            except Exception:
                pass


test_get_properties_property_id_ai_analysis()