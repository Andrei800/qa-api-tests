import logging, time
from typing import Dict
import pytest
from faker import Faker

from tests.schemas.user import user_schema, users_list_schema
from tests.utils.schema_validator import assert_schema
from tests.utils.http_asserts import assert_content_type_json, assert_charset_utf8

logger = logging.getLogger("tests")
fake = Faker()

def _now_suffix() -> str:
    return str(int(time.time() * 1000))

def _new_user_payload() -> Dict:
    return {
        "name": fake.name(),
        "email": f"{fake.user_name()}_{_now_suffix()}@example.com",
        "gender": fake.random_element(("male", "female")),
        "status": "active",
    }

@pytest.mark.positive
@pytest.mark.e2e
def test_user_e2e_chain(client):  # <-- берём фикстуру client
    # 1) POST
    create_payload = _new_user_payload()
    resp_post = client.create_user(create_payload)
    assert_content_type_json(resp_post.headers); assert_charset_utf8(resp_post.headers)
    assert resp_post.status_code == 201, f"Ожидали 201, получили {resp_post.status_code}: {resp_post.text}"
    data = resp_post.json()
    assert_schema(data, user_schema, name="POST /users")
    body_post = resp_post.json()
    user_id = body_post["id"]
    for k in ("name", "email", "gender", "status"):
        assert body_post.get(k) == create_payload[k]

    try:
        # 2) GET
        resp_get = client.get_user(user_id)
        assert_content_type_json(resp_get.headers); assert_charset_utf8(resp_get.headers)
        assert resp_get.status_code == 200
        data = resp_get.json()
        assert_schema(data, user_schema, name="GET /users/{id}")
        body_get = resp_get.json()
        for k in ("name", "email", "gender", "status"):
            assert body_get.get(k) == create_payload[k]

        # 3) PATCH
        patch_payload = {"name": f"{create_payload['name']} (updated)", "status": "inactive"}
        resp_patch = client.patch_user(user_id, patch_payload)
        assert_content_type_json(resp_patch.headers); assert_charset_utf8(resp_patch.headers)
        assert resp_patch.status_code == 200
        body_patch = resp_patch.json()
        assert_schema(data, user_schema, name="PATCH /users/{id}")
        assert body_patch.get("name") == patch_payload["name"]
        assert body_patch.get("status") == patch_payload["status"]

        # 4) DELETE
        resp_del = client.delete_user(user_id)
        # Content-Type на 204 может отсутствовать — это нормально
        assert resp_del.status_code == 204, f"Ожидали 204, получили {resp_del.status_code}: {resp_del.text}"

        # 5) GET after DELETE
        resp_get2 = client.get_user(user_id)
        assert resp_get2.status_code == 404, f"После удаления ожидали 404, получили {resp_get2.status_code}: {resp_get2.text}"
    finally:
        try:
            client.delete_user(user_id)
        except Exception:
            pass