import os
import pytest

def assert_status(resp, allowed: set[int], *, ci_tolerate_429=True):
    code = resp.status_code
    if code in allowed:
        return
    if ci_tolerate_429 and os.getenv("CI") == "true" and code == 429:
        pytest.xfail("CI rate limit: 429")
    assert code in allowed, f"Unexpected status {code}. Body: {getattr(resp, 'text', '')}"
