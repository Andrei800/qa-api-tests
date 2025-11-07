import logging
import time
import pytest
import requests

logger = logging.getLogger("tests")


def _assert_resp_time(resp: requests.Response, threshold: float, label: str):
    elapsed = resp.elapsed.total_seconds()
    logger.info("%s -> %s in %.3fs (threshold=%.3fs)", label, resp.status_code, elapsed, threshold)
    assert elapsed <= threshold, f"{label}: {elapsed:.3f}s превышает порог {threshold:.3f}s"


@pytest.mark.performance
def test_get_users_is_fast(base_url, api_headers, perf_threshold):
    resp = requests.get(f"{base_url}/users", headers=api_headers, params={"page": 1})
    assert resp.status_code == 200, f"GET /users: ожидали 200, получили {resp.status_code}: {resp.text}"
    _assert_resp_time(resp, perf_threshold, "GET /users?page=1")


@pytest.mark.performance
def test_post_get_delete_with_perf(base_url, api_headers, perf_threshold):
    now = int(time.time() * 1000)
    payload = {
        "name": f"Perf User {now}",
        "email": f"perf_{now}@example.com",
        "gender": "male",
        "status": "active",
    }
    r_post = requests.post(f"{base_url}/users", headers=api_headers, json=payload)
    assert r_post.status_code == 201, f"POST /users: ожидали 201, получили {r_post.status_code}: {r_post.text}"
    _assert_resp_time(r_post, perf_threshold, "POST /users")
    user_id = r_post.json()["id"]

    try:
        r_get = requests.get(f"{base_url}/users/{user_id}", headers=api_headers)
        assert r_get.status_code == 200, f"GET /users/{user_id}: ожидали 200, получили {r_get.status_code}: {r_get.text}"
        _assert_resp_time(r_get, perf_threshold, f"GET /users/{user_id}")

        r_patch = requests.patch(f"{base_url}/users/{user_id}", headers=api_headers, json={"status": "inactive"})
        assert r_patch.status_code == 200, f"PATCH /users/{user_id}: ожидали 200, получили {r_patch.status_code}: {r_patch.text}"
        _assert_resp_time(r_patch, perf_threshold, f"PATCH /users/{user_id}")
    finally:
        r_del = requests.delete(f"{base_url}/users/{user_id}", headers=api_headers)
        assert r_del.status_code in (204, 404), f"DELETE /users/{user_id}: ожидали 204/404, получили {r_del.status_code}: {r_del.text}"
        _assert_resp_time(r_del, perf_threshold, f"DELETE /users/{user_id}")