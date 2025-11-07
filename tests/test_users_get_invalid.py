import pytest
import requests
from tests.utils.neg_asserts import assert_client_error_or_xfail


invalid_ids = [
    pytest.param("", marks=pytest.mark.xfail(reason="BUG: пустой ID может вернуть список/200")),
    "abc", "123abc", "@!#", " ", None, 0, -1, 9_999_999_999,
]

@pytest.mark.negative
@pytest.mark.parametrize("user_id", invalid_ids, ids=lambda x: f"id={repr(x)}")
def test_get_user_with_invalid_id(base_url, api_headers, user_id):
    url = f"{base_url}/users/{user_id}"
    resp = requests.get(url, headers=api_headers)
    assert_client_error_or_xfail(resp, f"GET invalid id={user_id}")

    # Ожидаем 4xx, точно не 200/201.
    assert resp.status_code not in (200, 201), f"Unexpected 2xx для ID={user_id}. Ответ: {resp.text}"
    assert resp.status_code in {400, 401, 403, 404, 409, 422}, \
        f"Expected 4xx, got {resp.status_code} for ID={user_id}. Ответ: {resp.text}"