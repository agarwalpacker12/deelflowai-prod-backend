
# TestSprite AI Testing Report(MCP)

---

## 1️⃣ Document Metadata
- **Project Name:** deelflowai-backend
- **Date:** 2025-10-10
- **Prepared by:** TestSprite AI Team

---

## 2️⃣ Requirement Validation Summary

#### Test TC001
- **Test Name:** post properties create new property
- **Test Code:** [TC001_post_properties_create_new_property.py](./TC001_post_properties_create_new_property.py)
- **Test Error:** Traceback (most recent call last):
  File "<string>", line 18, in test_post_properties_create_new_property
AssertionError: access_token not in login response

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 90, in <module>
  File "<string>", line 21, in test_post_properties_create_new_property
AssertionError: Authentication failed: access_token not in login response

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/af44a59f-0a05-462e-8991-88dcf975edba/e96f8b0c-52ad-46e1-a765-8581cdb34768
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC002
- **Test Name:** get properties retrieve all properties
- **Test Code:** [TC002_get_properties_retrieve_all_properties.py](./TC002_get_properties_retrieve_all_properties.py)
- **Test Error:** Traceback (most recent call last):
  File "<string>", line 21, in get_basic_auth_token
AssertionError: access_token missing in login response

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 92, in <module>
  File "<string>", line 28, in test_get_properties_retrieve_all_properties
  File "<string>", line 25, in get_basic_auth_token
RuntimeError: Failed to get auth token: access_token missing in login response

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/af44a59f-0a05-462e-8991-88dcf975edba/7d66b0ef-1b59-4c4d-9006-c961601a70c9
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC003
- **Test Name:** get properties property id retrieve property details
- **Test Code:** [TC003_get_properties_property_id_retrieve_property_details.py](./TC003_get_properties_property_id_retrieve_property_details.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 61, in <module>
  File "<string>", line 15, in test_get_property_by_id_retrieve_property_details
AssertionError: access_token missing in login response

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/af44a59f-0a05-462e-8991-88dcf975edba/9fc2d0fe-1e62-4cbd-a64d-68af93b49cec
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC004
- **Test Name:** put properties property id update property
- **Test Code:** [TC004_put_properties_property_id_update_property.py](./TC004_put_properties_property_id_update_property.py)
- **Test Error:** Traceback (most recent call last):
  File "<string>", line 24, in test_tc004_put_properties_property_id_update_property
AssertionError: Access or refresh token missing in login response

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 114, in <module>
  File "<string>", line 26, in test_tc004_put_properties_property_id_update_property
AssertionError: Login API call failed: Access or refresh token missing in login response

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/af44a59f-0a05-462e-8991-88dcf975edba/2f6254c3-1f17-4af1-a7cd-5249aca56ce1
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC005
- **Test Name:** delete properties property id delete property
- **Test Code:** [TC005_delete_properties_property_id_delete_property.py](./TC005_delete_properties_property_id_delete_property.py)
- **Test Error:** Traceback (most recent call last):
  File "<string>", line 22, in get_auth_token
AssertionError: access_token not found in login response

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 134, in <module>
  File "<string>", line 53, in delete_property_test
  File "<string>", line 26, in get_auth_token
RuntimeError: Authentication failed: access_token not found in login response

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/af44a59f-0a05-462e-8991-88dcf975edba/b9a0440d-c6bd-4e1f-9218-07f6af4744a4
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC006
- **Test Name:** get properties property id ai analysis
- **Test Code:** [TC006_get_properties_property_id_ai_analysis.py](./TC006_get_properties_property_id_ai_analysis.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 88, in <module>
  File "<string>", line 22, in test_get_properties_property_id_ai_analysis
AssertionError: Tokens not found in login response

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/af44a59f-0a05-462e-8991-88dcf975edba/bcdc22e1-f9d1-46d4-96d4-e22c5b534192
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC007
- **Test Name:** post api auth login user login
- **Test Code:** [TC007_post_api_auth_login_user_login.py](./TC007_post_api_auth_login_user_login.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 125, in <module>
  File "<string>", line 30, in test_post_api_auth_login_user_login
AssertionError: access_token missing in login response

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/af44a59f-0a05-462e-8991-88dcf975edba/35937b8a-3c7d-4619-9cfd-579fc314b038
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC008
- **Test Name:** post api auth register user registration
- **Test Code:** [TC008_post_api_auth_register_user_registration.py](./TC008_post_api_auth_register_user_registration.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/af44a59f-0a05-462e-8991-88dcf975edba/c7936afb-b88d-4c52-8c74-25c1dde95316
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC009
- **Test Name:** get stats get dashboard statistics
- **Test Code:** [TC009_get_stats_get_dashboard_statistics.py](./TC009_get_stats_get_dashboard_statistics.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 136, in <module>
  File "<string>", line 25, in test_tc009_get_stats_dashboard_statistics
AssertionError: access_token not found in login response

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/af44a59f-0a05-462e-8991-88dcf975edba/9769f9e6-ddb7-4807-a2f4-9b502a3b606d
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC010
- **Test Name:** get total revenue get total revenue metrics
- **Test Code:** [TC010_get_total_revenue_get_total_revenue_metrics.py](./TC010_get_total_revenue_get_total_revenue_metrics.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 48, in <module>
  File "<string>", line 21, in test_get_total_revenue_metrics
AssertionError: access_token not found in login response

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/af44a59f-0a05-462e-8991-88dcf975edba/69eddcfa-07e9-4b0a-9e98-9301e387f4fe
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---


## 3️⃣ Coverage & Matching Metrics

- **10.00** of tests passed

| Requirement        | Total Tests | ✅ Passed | ❌ Failed  |
|--------------------|-------------|-----------|------------|
| ...                | ...         | ...       | ...        |
---


## 4️⃣ Key Gaps / Risks
{AI_GNERATED_KET_GAPS_AND_RISKS}
---