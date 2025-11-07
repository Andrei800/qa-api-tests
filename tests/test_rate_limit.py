import logging
import time
from collections import deque

import pytest
import requests

logger = logging.getLogger("tests")

def _hdr(resp, name: str):
    for k, v in resp.headers.items():
        if k.lower() == name.lower():
            return v
    return None

@pytest.mark.ratelimit
def test_rate_limit_burst_get_users(base_url, api_headers, rate_burst_count):
    statuses = []
    remaining_vals = []
    last_headers = {}
    tail = deque(maxlen=5)

    for i in range(rate_burst_count):
        resp = requests.get(f"{base_url}/users", headers=api_headers, params={"page": 1})
        statuses.append(resp.status_code)
        h_limit = _hdr(resp, "X-Rate-Limit-Limit")
        h_remaining = _hdr(resp, "X-Rate-Limit-Remaining")
        h_reset = _hdr(resp, "X-Rate-Limit-Reset")
        last_headers = {"limit": h_limit, "remaining": h_remaining, "reset": h_reset}

        if h_remaining is not None:
            try:
                rem = int(h_remaining)
                remaining_vals.append(rem)
                tail.append(rem)
            except ValueError:
                pass

        if i % 5 == 0 or resp.status_code == 429:
            logger.info("Burst %d/%d -> %s | remaining=%s, limit=%s, reset=%s",
                        i + 1, rate_burst_count, resp.status_code, h_remaining, h_limit, h_reset)
        if resp.status_code == 429:
            break
        time.sleep(0.05)

    if 429 in statuses:
        assert True
        return

    if remaining_vals:
        near_zero = all(x <= 1 for x in tail) if tail else False
        assert near_zero or min(remaining_vals) == 0, (
            f"Не поймали 429 и remaining не дошёл до 0. "
            f"min(remaining)={min(remaining_vals)}, последние={list(tail)}, headers={last_headers}"
        )
    else:
        pytest.xfail(
            "Сервис не возвращает X-Rate-Limit-* заголовки и не удалось получить 429 при burst-запросах. "
            "Проверьте политику лимитов API/токена."
        )