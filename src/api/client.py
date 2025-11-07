# src/api/client.py
from __future__ import annotations

import os
import time
import random
import datetime
import threading
import logging
from email.utils import parsedate_to_datetime

import requests
import backoff

log = logging.getLogger("api")


class ApiClient:
    """HTTP-клиент для публичного API с поддержкой 429 и троттлингом в CI."""

    # Глобальный "затвор" для ограничения QPS (только в CI)
    _lock = threading.Lock()
    _next_allowed_time = 0.0

    def __init__(self, base_url: str, token: str, timeout: float = 15.0) -> None:
        self.base = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        )

    @backoff.on_exception(
        backoff.expo,
        (requests.Timeout, requests.ConnectionError),
        max_time=30,
    )
    def request(self, method: str, path: str, **kw) -> requests.Response:
        """
        Универсальный запрос:
        - уважает Retry-After при 429
        - экспоненциальный backoff + небольшой джиттер
        - троттлинг в CI по RATE_LIMIT_QPS (по умолчанию 2 QPS)
        """
        url = f"{self.base}{path}"
        max_attempts = kw.pop("max_attempts", 6)
        base_delay = float(kw.pop("base_delay", 1.0))
        cap_delay = float(kw.pop("cap_delay", 20.0))

        for attempt in range(1, max_attempts + 1):
            # -------- THROTTLE: только в CI --------
            if os.getenv("CI") == "true":
                rate_qps = float(os.getenv("RATE_LIMIT_QPS", "2.0"))  # 2 запроса/сек
                min_interval = 1.0 / max(rate_qps, 0.1)
                with ApiClient._lock:
                    now = time.time()
                    if now < ApiClient._next_allowed_time:
                        time.sleep(ApiClient._next_allowed_time - now)
                    # обновляем ВСЕГДА, даже если не спали
                    ApiClient._next_allowed_time = time.time() + min_interval
            # ---------------------------------------

            resp = self.session.request(method, url, timeout=self.timeout, **kw)
            rt = resp.elapsed.total_seconds()
            log.debug("HTTP %s %s -> %s in %.3fs", method, path, resp.status_code, rt)

            # Если не 429 — возвращаем как есть
            if resp.status_code != 429:
                return resp

            # ===== Обработка 429 =====
            retry_after_header = resp.headers.get("Retry-After")
            delay = None

            # 1) Уважаем Retry-After, если есть
            if retry_after_header:
                raw = retry_after_header.strip()
                if raw.isdigit():
                    delay = float(raw)
                else:
                    try:
                        dt = parsedate_to_datetime(raw)
                        delay = max(
                            0.0,
                            (dt - datetime.datetime.now(tz=dt.tzinfo)).total_seconds(),
                        )
                    except Exception:
                        delay = None

            # 2) Иначе — экспоненциальный backoff с джиттером
            if delay is None:
                backoff_delay = min(base_delay * (2 ** (attempt - 1)), cap_delay)
                delay = backoff_delay + random.uniform(0.0, 0.3)

            if attempt == max_attempts:
                log.warning(
                    "429 after %d attempts, giving up (last delay=%.2fs)",
                    attempt,
                    delay,
                )
                return resp  # пусть тест решает сам (xfail/negative/и т.д.)

            log.info(
                "429 received. Attempt %d/%d. Sleeping for %.2fs (Retry-After=%s)",
                attempt,
                max_attempts,
                delay,
                retry_after_header,
            )
            time.sleep(delay)
            # ===== конец обработки 429 =====

        return resp  # теоретически недостижимо

    # -------- Удобные методы (CRUD) --------
    def users(self) -> requests.Response:
        return self.request("GET", "/users")

    def create_user(self, payload: dict) -> requests.Response:
        return self.request("POST", "/users", json=payload)

    def get_user(self, user_id: int | str) -> requests.Response:
        return self.request("GET", f"/users/{user_id}")

    def patch_user(self, user_id: int | str, payload: dict) -> requests.Response:
        return self.request("PATCH", f"/users/{user_id}", json=payload)

    def delete_user(self, user_id: int | str) -> requests.Response:
        return self.request("DELETE", f"/users/{user_id}")
