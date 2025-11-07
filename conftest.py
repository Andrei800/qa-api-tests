# conftest.py
import os, warnings, sys, time
import logging
import pytest
from api.client import ApiClient
from dotenv import load_dotenv
import logging
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)

# гарантируем, что src попадает в sys.path даже вне pytest
SRC_DIR = os.path.join(os.path.dirname(__file__), "src")
if os.path.isdir(SRC_DIR) and SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

try:
    # если client.py лежит в src/
    from api.client import ApiClient
except ModuleNotFoundError:
    # если клиент лежит в src/api/client.py
    from api.client import ApiClient

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
_TOKEN = os.getenv("TOKEN")
logger = logging.getLogger("tests")
def _build_headers(token: str):
    if not token:
        return {"Content-Type": "application/json"}  # без авторизации
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
warnings.warn(
    "Legacy import from conftest (BASE_URL, headers) is deprecated. "
    "Use fixtures: base_url, api_headers.",
    DeprecationWarning,
    stacklevel=2,
)

headers = _build_headers(_TOKEN)

def _mask_secret(s: str, keep: int = 4) -> str:
    if not s:
        return "<missing>"
    return "*" * max(len(s) - keep, 0) + s[-keep:]

@pytest.fixture(scope="session")
def base_url() -> str:
    url = os.getenv("BASE_URL")
    if not url:
        pytest.exit("BASE_URL not set (add to .env)")
    return url

@pytest.fixture(scope="session")
def token() -> str:
    t = os.getenv("TOKEN")
    if not t:
        pytest.exit("TOKEN not set (add to .env)")
    logger.info("Auth token loaded: %s", _mask_secret(t))
    return t

@pytest.fixture
def api_headers(token):
    # В логах не показываем Authorization целиком
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
# ==== performance & ratelimit options ====
def pytest_addoption(parser):
    parser.addoption(
        "--perf-threshold",
        action="store",
        type=float,
        default=float(os.getenv("PERF_THRESHOLD_SECONDS", 1.5)),
        help="Макс. допустимое время ответа (сек). По умолчанию PERF_THRESHOLD_SECONDS или 1.5."
    )
    parser.addoption(
        "--rate-burst-count",
        action="store",
        type=int,
        default=int(os.getenv("RATE_BURST_COUNT", 30)),
        help="Сколько быстрых запросов отправить для проверки rate limit (дефолт 30)."
    )

@pytest.fixture(scope="session")
def perf_threshold(request) -> float:
    return float(request.config.getoption("--perf-threshold"))

@pytest.fixture(scope="session")
def rate_burst_count(request) -> int:
    return int(request.config.getoption("--rate-burst-count"))

@pytest.fixture(scope="session")
def client(base_url, token) -> "ApiClient":
    """Единый HTTP‑клиент для тестов с таймаутами/ретраями."""
    return ApiClient(base_url=base_url, token=token, timeout=15)

def user_fixture(client):
    """Создаёт пользователя и удаляет его после теста."""
    payload = {
        "name": "QA Temp",
        "gender": "male",
        "email": f"qa_{int(time.time()*1000)}@example.com",
        "status": "active",
    }
    resp = client.create_user(payload)
    assert resp.status_code in {201, 200}, f"Create failed: {resp.status_code} {resp.text}"
    user = resp.json()
    try:
        yield user
    finally:
        try:
            del_resp = client.delete_user(user.get("id"))
            # не валим тест, если уже удалён/не найден
            if del_resp.status_code not in {200, 204, 404}:
                print(f"Cleanup delete returned {del_resp.status_code}: {del_resp.text}")
        except Exception:
            pass
