from typing import Mapping
from urllib.parse import urlparse, parse_qs

def _h(headers: Mapping, name: str):
    for k, v in headers.items():
        if k.lower() == name.lower():
            return v
    return None

def assert_content_type_json(headers: Mapping):
    ct = _h(headers, "Content-Type")
    assert ct is not None, "Отсутствует Content-Type"
    assert "application/json" in ct.lower(), f"Ожидали JSON, получили Content-Type={ct}"

def assert_charset_utf8(headers: Mapping):
    ct = _h(headers, "Content-Type") or ""
    assert "charset" in ct.lower() and "utf-8" in ct.lower(), f"Ожидали charset=utf-8 в Content-Type, получили {ct}"

def assert_cors_permissive(headers: Mapping):
    allow = _h(headers, "Access-Control-Allow-Origin")
    assert allow in ("*", "https://example.com", None), f"Неожиданный CORS: Access-Control-Allow-Origin={allow}"

def parse_link_header(headers: Mapping):
    """
    Разбирает RFC5988 Link: <url1>; rel="next", <url2>; rel="last", ...
    Возвращает dict: {rel: url}
    """
    link = _h(headers, "Link")
    if not link:
        return {}
    parts = [p.strip() for p in link.split(",")]
    rels = {}
    for p in parts:
        if "<" not in p or ">" not in p:
            continue
        url = p[p.find("<")+1 : p.find(">")]
        if 'rel=' in p:
            rel = p.split('rel=')[-1].strip().strip('"').strip("'")
            rels[rel] = url
    return rels

def page_of(url: str) -> int | None:
    q = parse_qs(urlparse(url).query)
    try:
        return int(q.get("page", [None])[0])
    except (TypeError, ValueError):
        return None