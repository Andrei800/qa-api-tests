import pytest
import requests

@pytest.mark.positive
def test_patch_user(user_fixture, base_url, api_headers):
    user_id = user_fixture["id"]
    patch_data = {"name": "Updated Name"}
    resp = requests.patch(f"{base_url}/users/{user_id}", json=patch_data, headers=api_headers)

    assert resp.status_code == 200, f"PATCH ожидали 200, получили {resp.status_code}: {resp.text}"
    assert resp.json()["name"] == "Updated Name", f"name не обновился: {resp.text}"

@pytest.mark.positive
def test_get_user(user_fixture, base_url, api_headers):
    user_id = user_fixture["id"]
    resp = requests.get(f"{base_url}/users/{user_id}", headers=api_headers)

    assert resp.status_code == 200, f"GET ожидали 200, получили {resp.status_code}: {resp.text}"
    assert resp.json()["email"] == user_fixture["email"], "email в ответе не совпадает с созданным пользователем"