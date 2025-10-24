import requests

BASE_URL = "http://localhost:8140"
REGISTER_ENDPOINT = f"{BASE_URL}/api/auth/register"
TIMEOUT = 30


def test_post_api_auth_register_user_registration():
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "first_name": "Arpan",
        "last_name": "Sarkar",
        "organization_name": "Arpan Org",
        "phone": "1234567890",
        "email": "arpan.sarkar.test+unique@example.com",
        "password": "StrongPass!123"
    }

    try:
        response = requests.post(REGISTER_ENDPOINT, json=payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request to register user failed: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Further checks: response should indicate success
    try:
        json_resp = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    # As per PRD, no specific schema given except 200 returns "Registration successful"
    # So check if response body contains this or at least a success indication
    success_str = "Registration successful"
    response_text = response.text.lower()
    assert success_str.lower() in response_text or response.ok, "Registration not reported successful"


test_post_api_auth_register_user_registration()