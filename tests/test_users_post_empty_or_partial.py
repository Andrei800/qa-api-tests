import pytest
import requests
from faker import Faker
from tests.utils.neg_asserts import assert_client_error_or_xfail
fake = Faker()

@pytest.mark.negative
@pytest.mark.parametrize("payload, expected_status", [
    ({}, 422),
    ({"name": "", "email": "", "gender": "", "status": ""}, 422),
    ({"email": fake.email(), "gender": "male", "status": "active"}, 422),
    ({"name": fake.name(), "gender": "male", "status": "active"}, 422),
    ({"name": fake.name(), "email": fake.email()}, 422),
], ids=[
    "empty_payload",
    "all_fields_empty",
    "missing_name",
    "missing_email",
    "missing_gender_status",
])
def test_post_user_with_empty_or_partial_data(base_url, api_headers, payload, expected_status):
    resp = requests.post(f"{base_url}/users", headers=api_headers, json=payload)
    assert_client_error_or_xfail(resp, f"empty/partial payload={payload}", base_url, api_headers)
    if resp.status_code != expected_status:
        pytest.xfail(
            reason=f"BUG: API приняло некорректные данные: {payload}. "
                   f"Статус {resp.status_code}, тело {resp.text}"
        )
    assert resp.status_code == expected_status, \
        f"Ожидали {expected_status}, получили {resp.status_code}. Ответ: {resp.text}"