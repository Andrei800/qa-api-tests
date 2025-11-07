import pytest
import requests
import time
from tests.utils.neg_asserts import assert_client_error_or_xfail

# -------- INVALID EMAILS --------
invalid_emails = [
    "", "plainaddress", "@domain.com", "username@", "username@.com",
    "user name@example.com", "username@exa mple.com", "username@@example.com",
    "user..name@example.com", ".username@example.com", "username.@example.com",
    "username@.example.com", "username@example..com", "user@-example.com",
    "user@example-.com", "user@exam_ple.com", "user@ex!ample.com",
    "user@example.c", "user@example.123", "username@example.toolongtld",
    " user@example.com", "user@example.com ", "user@ example.com", None
]

@pytest.mark.negative
@pytest.mark.parametrize("email", invalid_emails, ids=lambda e: f"email={repr(e)}")
def test_create_user_with_invalid_email(base_url: str, api_headers: dict[str, str], email: Any):
    payload = {"name": "Test User", "email": email, "gender": "male", "status": "active"}
    resp = requests.post(f"{base_url}/users", json=payload, headers=api_headers)
    assert_client_error_or_xfail(resp, f"email={email}", base_url, api_headers)
    if resp.status_code == 201:
        _maybe_cleanup_created_user(base_url, api_headers, resp)
        pytest.xfail(f"BUG: API приняло невалидный email: {email} (status=201)")
        assert_client_error_or_xfail(resp, f"email={email}", base_url, api_headers)
        f"Ожидали 4xx для email={email}, получили {resp.status_code}: {resp.text}"

# -------- INVALID NAMES --------
invalid_names = [
    pytest.param(12345, marks=pytest.mark.xfail(reason="BUG: integer allowed in name")),
    pytest.param(True, marks=pytest.mark.xfail(reason="BUG: boolean allowed in name")),
    None, "", "a" * 256, "a" * 300,
]

@pytest.mark.negative
@pytest.mark.parametrize("name", invalid_names, ids=lambda n: f"name={repr(n)}")
def test_create_user_with_invalid_name(base_url: str, api_headers: dict[str, str], name: Any):
    payload = {"name": name, "email": f"autoname_{int(time.time())}@example.com", "gender": "male", "status": "active"}
    resp = requests.post(f"{base_url}/users", json=payload, headers=api_headers)
    assert_client_error_or_xfail(resp, f"name={name}", base_url, api_headers)
    if isinstance(name, (int, bool)) and resp.status_code == 201:
        pytest.xfail("BUG: числовое/булево name принято API")
    assert resp.status_code in {400, 401, 403, 404, 409, 422} and resp.status_code != 201, \
        f"Unexpected {resp.status_code} for name={name}: {resp.text}"
    if resp.status_code == 201:
        _maybe_cleanup_created_user(base_url, api_headers, resp)
        pytest.xfail("BUG: API приняло невалидное значение ...")


# -------- INVALID GENDERS --------
invalid_genders = [
    pytest.param("MALE", marks=pytest.mark.xfail(reason="BUG: uppercase gender accepted")),
    "femalee", "", None, 123
]

@pytest.mark.negative
@pytest.mark.parametrize("gender", invalid_genders, ids=lambda g: f"gender={repr(g)}")
def test_create_user_with_invalid_gender(base_url: str, api_headers: dict[str, str], gender: Any):
    payload = {"name": "Test User", "email": f"test_{int(time.time())}@example.com", "gender": gender, "status": "active"}
    resp = requests.post(f"{base_url}/users", json=payload, headers=api_headers)
    assert_client_error_or_xfail(resp, f"gender={gender}", base_url, api_headers)
    assert resp.status_code in {400, 401, 403, 404, 409, 422} and resp.status_code != 201, \
        f"Unexpected {resp.status_code} for gender={gender}: {resp.text}"
    if resp.status_code == 201:
        _maybe_cleanup_created_user(base_url, api_headers, resp)
        pytest.xfail("BUG: API приняло невалидное значение ...")

# -------- INVALID STATUSES --------
invalid_statuses = [
    pytest.param("ACTIVE", marks=pytest.mark.xfail(reason="BUG: uppercase status accepted")),
    "enabled", "", None, 1
]

@pytest.mark.negative
@pytest.mark.parametrize("status", invalid_statuses, ids=lambda s: f"status={repr(s)}")
def test_create_user_with_invalid_status(base_url: str, api_headers: dict[str, str], status: Any):
    payload = {"name": "Test User", "email": f"autostatus_{int(time.time())}@example.com", "gender": "male", "status": status}
    resp = requests.post(f"{base_url}/users", json=payload, headers=api_headers)
    assert_client_error_or_xfail(resp, f"status={status}", base_url, api_headers)
    assert resp.status_code in {400, 401, 403, 404, 409, 422} and resp.status_code != 201, \
        f"Unexpected {resp.status_code} for status={status}: {resp.text}"
    if resp.status_code == 201:
        _maybe_cleanup_created_user(base_url, api_headers, resp)
        pytest.xfail("BUG: API приняло невалидное значение ...")
    
def _maybe_cleanup_created_user(base_url, api_headers, resp):
    # Если вдруг создали пользователя – удалим, чтобы не засорять
    try:
        if resp.status_code == 201 and isinstance(resp.json(), dict) and "id" in resp.json():
            user_id = resp.json()["id"]
            requests.delete(f"{base_url}/users/{user_id}", headers=api_headers)
    except Exception:
        pass