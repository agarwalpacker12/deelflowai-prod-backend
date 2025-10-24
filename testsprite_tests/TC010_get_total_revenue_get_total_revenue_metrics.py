import requests

BASE_URL = "http://localhost:8140"
LOGIN_ENDPOINT = f"{BASE_URL}/api/auth/login"
TOTAL_REVENUE_ENDPOINT = f"{BASE_URL}/total-revenue/"

USERNAME = "arpansarkar@gmail.com"
PASSWORD = "arpan051992"
TIMEOUT = 30

def test_get_total_revenue_metrics():
    try:
        # Step 1: Authenticate user to get access token
        login_payload = {
            "email": USERNAME,
            "password": PASSWORD
        }
        login_response = requests.post(LOGIN_ENDPOINT, json=login_payload, timeout=TIMEOUT)
        assert login_response.status_code == 200, f"Login failed with status {login_response.status_code}"
        login_data = login_response.json()
        assert "access_token" in login_data, "access_token not found in login response"
        assert "refresh_token" in login_data, "refresh_token not found in login response"
        access_token = login_data["access_token"]

        # Step 2: Use access token to authorize GET /total-revenue/
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        response = requests.get(TOTAL_REVENUE_ENDPOINT, headers=headers, timeout=TIMEOUT)
        assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        resp_json = response.json()

        # Validate response structure and fields
        assert isinstance(resp_json, dict), "Response is not a JSON object"
        assert "status" in resp_json, "'status' field missing in response"
        assert resp_json["status"] == "success", f"Unexpected status value: {resp_json['status']}"
        assert "data" in resp_json, "'data' field missing in response"
        data = resp_json["data"]
        assert isinstance(data, dict), "'data' field is not an object"
        assert "total_revenue" in data, "'total_revenue' missing in data"
        assert isinstance(data["total_revenue"], (int, float)), "'total_revenue' is not a number"
        assert "change_percentage" in data, "'change_percentage' missing in data"
        assert isinstance(data["change_percentage"], (int, float)), "'change_percentage' is not a number"
    except requests.exceptions.RequestException as e:
        assert False, f"Request failed with exception: {e}"

test_get_total_revenue_metrics()