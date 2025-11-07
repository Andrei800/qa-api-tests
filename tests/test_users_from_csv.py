import pytest
from src.utils.data_loader import load_csv

@pytest.mark.negative
@pytest.mark.parametrize("payload", load_csv("users_invalid.csv"))
def test_post_user_from_csv(client, payload):
    """Тестируем POST /users с невалидными данными из CSV"""
    resp = client.create_user(payload)

    # Проверка, что API не принимает невалидные данные
    assert resp.status_code in [400, 422], (
        f"Ожидали 400/422 для {payload}, получили {resp.status_code}: {resp.text}"
    )

    # Проверим, что сообщение ошибки есть
    assert "message" in resp.text.lower(), f"Нет сообщения об ошибке: {resp.text}"
