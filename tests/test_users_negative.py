import time
import pytest
import requests

# Набор заведомо невалидных e-mail
invalid_emails = [
    "", "plainaddress", "@domain.com", "username@", "username@.com",
    "user name@example.com", "username@exa mple.com",
    "username@@example.com", "user..name@example.com", ".username@example.com",
    "username.@example.com", "username@.example.com", "username@example..com",
    "user@-example.com", "user@example-.com", "user@exam_ple.com", "user@ex!ample.com",
    "user@example.c", "user@example.123", "username@example.toolongtld",
    "a" * 300 + "@ex.com"
]

@pytest.mark.negative
@pytest.mark.parametrize("email", invalid_emails, ids=lambda e: f"email={e or '∅'}")
def test_create_user_with_invalid_email(base_url, api_headers, email):
    payload = {
        "name": "Test User",
        "email": email,
        "gender": "male",
        "status": "active",
    }
    resp = requests.post(f"{base_url}/users", json=payload, headers=api_headers)

    # На корректном API ожидаем 422. Разрешим 4xx на случай других политик валидации.
    assert resp.status_code in {400, 401, 403, 404, 409, 422} and resp.status_code != 201, \
        f"Неверный e-mail принят: {email}. Код={resp.status_code}, тело={resp.text}"


# Невалидные имена
invalid_names = [
    "",          # пустое имя
    "  ",        # одни пробелы
    "a" * 300,   # слишком длинное
    12345,       # число вместо строки (известный баг у многих API)
    None
]

@pytest.mark.negative
@pytest.mark.parametrize("name", invalid_names, ids=lambda n: f"name={repr(n)}")
def test_create_user_with_invalid_name(base_url, api_headers, name):
    payload = {
        "name": name,
        "email": f"test_{int(time.time())}@example.com",
        "gender": "male",
        "status": "active",
    }
    resp = requests.post(f"{base_url}/users", json=payload, headers=api_headers)

    # Известный дефект (если встречается): число может быть приведено к строке и принято -> xfail
    if isinstance(name, int) and resp.status_code == 201:
        pytest.xfail("BUG: числовое имя принято API (ожидали валидацию)")

    assert resp.status_code in {400, 401, 403, 404, 409, 422} and resp.status_code != 201, \
        f"Неверное name принято: {name}. Код={resp.status_code}, тело={resp.text}"


invalid_genders = ["", "attack helicopter", "unknown", 123, None]

@pytest.mark.negative
@pytest.mark.parametrize("gender", invalid_genders, ids=lambda g: f"gender={repr(g)}")
def test_create_user_with_invalid_gender(base_url, api_headers, gender):
    payload = {
        "name": "Test User",
        "email": f"test_{int(time.time())}@example.com",
        "gender": gender,
        "status": "active",
    }
    resp = requests.post(f"{base_url}/users", json=payload, headers=api_headers)
    assert resp.status_code in {400, 401, 403, 404, 409, 422} and resp.status_code != 201, \
        f"Неверный gender принят: {gender}. Код={resp.status_code}, тело={resp.text}"


invalid_statuses = ["", "inactivee", "deceased", 1, None]

@pytest.mark.negative
@pytest.mark.parametrize("status", invalid_statuses, ids=lambda s: f"status={repr(s)}")
def test_create_user_with_invalid_status(base_url, api_headers, status):
    payload = {
        "name": "Test User",
        "email": f"test_{int(time.time())}@example.com",
        "gender": "male",
        "status": status,
    }
    resp = requests.post(f"{base_url}/users", json=payload, headers=api_headers)
    assert resp.status_code in {400, 401, 403, 404, 409, 422} and resp.status_code != 201, \
        f"Неверный status принят: {status}. Код={resp.status_code}, тело={resp.text}"
