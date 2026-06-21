"""Stress-test: verify every route renders or redirects correctly."""

import pytest
import httpx

BASE = "http://127.0.0.1:9999"
PROTECTED_REDIRECT = {302, 303, 307}

try:
    client = httpx.Client(base_url=BASE, timeout=3)
    resp = client.get("/health")
    assert resp.status_code == 200
except Exception:
    pytest.skip(f"Server not running on {BASE}", allow_module_level=True)


def _check(method, path, expected):
    url = f"{BASE}{path}"
    if method == "GET":
        r = client.get(url, follow_redirects=False)
    else:
        r = client.post(url, follow_redirects=False)
    assert r.status_code in (expected if isinstance(expected, set) else {expected}), (
        f"{method} {path}: expected {expected}, got {r.status_code}"
    )


PUBLIC_ROUTES = [
    ("Landing", "GET", "/", 200),
    ("Health", "GET", "/health", 200),
    ("Login", "GET", "/auth/login", 200),
    ("Signup", "GET", "/auth/signup", 200),
    ("Logout", "GET", "/auth/logout", PROTECTED_REDIRECT),
    ("Leaderboard", "GET", "/leaderboard", {200, 302, 303}),
    ("Public goal", "GET", "/public/nonexistent", {200, 404}),
]


@pytest.mark.parametrize("name,method,path,expected", PUBLIC_ROUTES)
def test_public_routes(name, method, path, expected):
    _check(method, path, expected)


PROTECTED_GET = [
    ("Dashboard", "/dashboard"),
    ("Goals list", "/goals"),
    ("New goal form", "/goals/new"),
    ("Goal detail", "/goals/nonexistent"),
    ("Edit goal", "/goals/nonexistent/edit"),
    ("Checkin picker", "/checkin"),
    ("Checkin for goal", "/checkin/nonexistent"),
    ("Settings", "/settings"),
    ("Onboarding", "/onboarding"),
]


@pytest.mark.parametrize("name,path", PROTECTED_GET)
def test_protected_get_routes(name, path):
    _check("GET", path, PROTECTED_REDIRECT)


PROTECTED_POST = [
    ("Create goal", "/goals/create"),
    ("Edit goal", "/goals/nonexistent/edit"),
    ("Change status", "/goals/nonexistent/status"),
    ("Delete goal", "/goals/nonexistent/delete"),
    ("Toggle share", "/goals/nonexistent/share"),
    ("Invite partner", "/goals/nonexistent/partner"),
    ("Log checkin", "/checkin/log"),
    ("Update settings", "/settings"),
    ("Toggle leaderboard", "/settings/leaderboard"),
    ("Submit onboarding", "/onboarding"),
]


@pytest.mark.parametrize("name,path", PROTECTED_POST)
def test_protected_post_routes(name, path):
    _check("POST", path, PROTECTED_REDIRECT)
