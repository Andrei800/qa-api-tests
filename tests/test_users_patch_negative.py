import pytest
import requests
from src.utils.asserts import assert_status
from tests.utils.neg_asserts import assert_client_error_or_xfail

invalid_ids = [
    -1, 0, 999_999_999, "abc", "@@#",
    pytest.param("", marks=pytest.mark.xfail(reason="BUG: пустой ID даёт неожиданный ответ")),
]

invalid_payloads = [
    {"name": 12345},
    {"email": "invalidemail"},
    {"status": "ENABLED"},
    {"gender": "robot"},
    {"status": ""},
    {"gender": ""},
    {"email": ""},
    {"name": ""},
    {"email": None},
    {"name": None},
    {},
]

@pytest.mark.negative
@pytest.mark.parametrize("user_id", invalid_ids, ids=lambda x: f"id={repr(x)}")
@pytest.mark.parametrize("payload", invalid_payloads, ids=lambda p: "payload=" + (",".join(f"{k}={repr(v)}" for k, v in p.items()) if p else "{}"))
def test_patch_user_with_invalid_id_or_data(base_url, api_headers, user_id, payload):
    url = f"{base_url}/users/{user_id}"
    resp = requests.patch(url, headers=api_headers, json=payload)
    assert_client_error_or_xfail(resp, f"PATCH invalid id={user_id}, payload={payload}")
    # Для невалидных ID/тела — 4xx; точно не 200/201
    assert resp.status_code not in (200, 201), f"Unexpected 2xx для ID={user_id}, payload={payload}"
    allowed = {400, 401, 403, 404, 409, 422}
    assert_status(resp, allowed, ci_tolerate_429=True)