import pytest
import requests
from tests.utils.neg_asserts import assert_client_error_or_xfail

invalid_ids = [
    -1, 0, 999_999_999, "abc", "@@#",
    pytest.param("", marks=pytest.mark.xfail(reason="BUG: пустой ID может дать некорректный ответ")),
]

@pytest.mark.negative
@pytest.mark.parametrize("user_id", invalid_ids, ids=lambda x: f"id={repr(x)}")
def test_delete_user_with_invalid_id(base_url, api_headers, user_id):
    url = f"{base_url}/users/{user_id}"
    resp = requests.delete(url, headers=api_headers)
    assert_client_error_or_xfail(resp, f"DELETE invalid id={user_id}")

    # Для невалидных/несуществующих ID ожидаем 4xx; точно не 200/201.
    assert resp.status_code not in (200, 201), f"Unexpected 2xx для ID={user_id}. Ответ: {resp.text}"
    assert resp.status_code in {400, 401, 403, 404, 409, 422}, \
        f"Неожиданный код {resp.status_code} для ID={user_id}. Ответ: {resp.text}"
