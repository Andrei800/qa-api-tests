
import pytest, time, random, datetime
import os, threading
import backoff, requests, logging
from email.utils import parsedate_to_datetime  # для Retry-After: HTTP-date

log = logging.getLogger("api")
class ApiClient:
    _lock = threading.Lock()
    _next_allowed_time = 0.0  # timestamp, когда можно делать следующий запрос
    def __init__(self, base_url, token, timeout=15):
        self.base = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })
        self.timeout = timeout

    # внутри класса ApiClient

@backoff.on_exception(
    backoff.expo,
    (requests.Timeout, requests.ConnectionError),
    max_time=30,
)
def request(self, method, path, **kw):
    """
    Универсальный запрос с поддержкой 429 Too Many Requests.
    - уважает Retry-After (число секунд или HTTP-date)
    - экспоненциальный backoff с джиттером и верхней границей
    """
    url = f"{self.base}{path}"
    max_attempts = kw.pop("max_attempts", 6)     # можно переопределить из теста
    base_delay = kw.pop("base_delay", 1.0)       # старт задержки
    cap_delay = kw.pop("cap_delay", 20.0)        # максимум задержки

    for attempt in range(1, max_attempts + 1):
        if os.getenv("CI") == "true":  # активируем только в GitHub Actions
            rate_qps = float(os.getenv("RATE_LIMIT_QPS", "2.0"))  # 2 запроса/сек по умолчанию
            min_interval = 1.0 / rate_qps
            with ApiClient._lock:
                now = time.time()
                if now < ApiClient._next_allowed_time:
                    delay = ApiClient._next_allowed_time - now
                    time.sleep(delay)
                    ApiClient._next_allowed_time = time.time() + min_interval
        resp = self.session.request(method, url, timeout=self.timeout, **kw)
        rt = resp.elapsed.total_seconds()
        log.debug("HTTP %s %s -> %s in %.3fs", method, path, resp.status_code, rt)

        # если это не 429 — сразу возвращаем
        if resp.status_code != 429:
            return resp

        # ===== обработка 429 =====
        # 1) пробуем уважить Retry-After
        retry_after_header = resp.headers.get("Retry-After")
        delay = None
        if retry_after_header:
            retry_after_header = retry_after_header.strip()
            # формат: секундами
            if retry_after_header.isdigit():
                delay = int(retry_after_header)
            else:
                # формат: HTTP-date
                try:
                    dt = parsedate_to_datetime(retry_after_header)
                    # переводим в delta относительно текущего времени
                    delay = max(0, (dt - datetime.datetime.utcnow().replace(tzinfo=dt.tzinfo)).total_seconds())
                except Exception:
                    delay = None

        # 2) если нет валидного Retry-After — экспоненциальный backoff
        if delay is None:
            backoff_delay = min(base_delay * (2 ** (attempt - 1)), cap_delay)
            jitter = random.uniform(0, 0.3)  # небольшой джиттер для рассинхронизации
            delay = backoff_delay + jitter

        # если это была последняя попытка — выходим с тем, что есть
        if attempt == max_attempts:
            log.warning("429 after %d attempts, giving up (last delay=%.2fs)", attempt, delay)
            return resp  # пусть тест сам решит: xfail/negative и т.п.

        log.info("429 received. Attempt %d/%d. Sleeping for %.2fs (Retry-After=%s)",
                 attempt, max_attempts, delay, retry_after_header)
        time.sleep(delay)

    # теоретически недостижимо
    return resp

 # удобные методы
def users(self): return self.request("GET", "/users")
def create_user(self, payload): return self.request("POST", "/users", json=payload)
def get_user(self, id): return self.request("GET", f"/users/{id}")
def patch_user(self, id, payload): return self.request("PATCH", f"/users/{id}", json=payload)
def delete_user(self, id): return self.request("DELETE", f"/users/{id}")


try:
    # если client.py лежит прямо в src/
    from api.client import ApiClient
    # если переложишь в src/api/client.py — меняем на:
    # from api.client import ApiClient
except Exception as e:
    raise RuntimeError(f"Cannot import ApiClient: {e}")

@pytest.fixture(scope="session")
def client(base_url, token) -> "ApiClient":
    return ApiClient(base_url=base_url, token=token, timeout=15)
