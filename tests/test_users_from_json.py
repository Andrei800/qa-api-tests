import logging
import pytest
from src.utils.data_loader import load_json
from tests.utils.neg_asserts import assert_client_error_or_xfail

log = logging.getLogger(__name__)

def _case_id(p: dict) -> str:
    return f"{p.get('name') or 'noname'}__{p.get('email') or 'noemail'}"

def _has_error_message(resp) -> bool:
    # GoRest может вернуть dict или list[dict] вида [{"message": "..."}]
    try:
        body = resp.json()
    except ValueError:
        return "message" in resp.text.lower()

    if isinstance(body, dict):
        return "message" in {k.lower() for k in body.keys()} or "message" in str(body).lower()
    if isinstance(body, list) and body and isinstance(body[0], dict):
        return "message" in {k.lower() for k in body[0].keys()} or "message" in str(body[0]).lower()
    return "message" in str(body).lower()

@pytest.mark.negative
@pytest.mark.parametrize("payload", load_json("users_invalid.json"), ids=_case_id)
def test_post_user_from_json(client, payload):
    """Негативные тесты POST /users с JSON-данными"""
    log.info("JSON payload: %s", payload)

    resp = client.create_user(payload)

    # 1) Статус: допускаем 400/422 как корректный негативный ответ
    assert resp.status_code in (400, 422), (
        f"Некорректный статус для {payload}: {resp.status_code}\nBody: {resp.text}"
    )

    # 2) В ответе должно быть сообщение об ошибке
    assert _has_error_message(resp), f"Ответ не содержит сообщения об ошибке: {resp.text}"