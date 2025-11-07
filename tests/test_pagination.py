import logging
import pytest
import requests

from tests.schemas.user import users_list_schema
from tests.utils.schema_validator import assert_schema
from tests.utils.http_asserts import (
    assert_content_type_json, assert_charset_utf8,
    parse_link_header, page_of
)

logger = logging.getLogger("tests")

@pytest.mark.positive
def test_users_list_pagination_and_link(base_url, api_headers):
    params1 = {"page": 1, "per_page": 20}
    r1 = requests.get(f"{base_url}/users", headers=api_headers, params=params1)
    assert r1.status_code == 200, f"GET /users?page=1 -> {r1.status_code}: {r1.text}"
    assert_content_type_json(r1.headers)
    assert_charset_utf8(r1.headers)

    body1 = r1.json()
    assert_schema(body1, users_list_schema, name="GET /users?page=1")
    assert 1 <= len(body1) <= 20, f"Неожиданное количество элементов: {len(body1)}"

    # Всегда проверяем вторую страницу напрямую (без обязательного Link)
    params2 = {"page": 2, "per_page": 20}
    r2 = requests.get(f"{base_url}/users", headers=api_headers, params=params2)
    assert r2.status_code == 200, f"GET /users?page=2 -> {r2.status_code}: {r2.text}"
    assert_content_type_json(r2.headers)
    assert_charset_utf8(r2.headers)

    body2 = r2.json()
    assert_schema(body2, users_list_schema, name="GET /users?page=2")
    assert 1 <= len(body2) <= 20, f"Неожиданное количество элементов: {len(body2)}"

    ids1 = {u["id"] for u in body1}
    ids2 = {u["id"] for u in body2}
    assert ids1 != ids2, "Страница 1 и страница 2 не должны содержать одинаковый набор id"

    # Если сервер вернул Link — валидируем корректность
    links = parse_link_header(r1.headers)
    if links:
        next_url = links.get("next")
        if next_url:
            p = page_of(next_url)
            assert p and p >= 2, f"Link next должен указывать на страницу >=2, получили {next_url}"
            r_next = requests.get(next_url, headers=api_headers)
            assert r_next.status_code == 200, f"GET next -> {r_next.status_code}: {r_next.text}"
            assert_content_type_json(r_next.headers)
            assert_charset_utf8(r_next.headers)
            assert_schema(r_next.json(), users_list_schema, name="GET next(page)")
    else:
        logger.warning("Сервер не вернул Link header — валидируем пагинацию прямыми запросами page=1/2.")
    assert_schema(r1.json(), users_list_schema, name="GET /users?page=1")
    assert_schema(r2.json(), users_list_schema, name="GET /users?page=2")