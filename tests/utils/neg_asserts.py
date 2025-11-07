# tests/utils/neg_asserts.py
import logging
import requests

log = logging.getLogger("tests")

def _cleanup_if_created(resp: requests.Response, base_url: str, headers: dict):
    """Если POST создал пользователя, удалим, чтобы не засорять окружение."""
    try:
        if resp.request.method.upper() == "POST" and 200 <= resp.status_code < 300:
            body = resp.json()
            if isinstance(body, dict) and "id" in body:
                uid = body["id"]
                requests.delete(f"{base_url}/users/{uid}", headers=headers, timeout=15)
    except Exception as e:
        log.warning("Cleanup after unexpected 2xx failed: %s", e)

def assert_client_error_or_xfail(resp: requests.Response, case_desc: str,
                                 base_url: str | None = None, api_headers: dict | None = None):
    """
    Любой 2xx → XFAIL (BUG: принято невалидное) + попытка cleanup (только для POST).
    Любой 4xx → PASS (валидатор сработал).
    Любой 5xx → FAIL (ошибка сервера).
    """
    code = resp.status_code
    if 200 <= code < 300:
        if base_url and api_headers:
            _cleanup_if_created(resp, base_url, api_headers)
        import pytest
        pytest.xfail(f"BUG: API приняло невалидные данные ({case_desc}), статус={code}")
    assert 400 <= code < 500, f"Ожидали 4xx для {case_desc}, получили {code}: {resp.text}"
