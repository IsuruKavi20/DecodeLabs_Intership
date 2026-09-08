import hashlib
import io
import urllib.error

import pytest

from src import hibp

PASSWORD = "password"
_DIGEST = hashlib.sha1(PASSWORD.encode()).hexdigest().upper()
PREFIX, SUFFIX = _DIGEST[:5], _DIGEST[5:]


class _FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False


def _install_fake_urlopen(monkeypatch, body: str, captured: dict):
    def fake_urlopen(request, timeout=None):
        captured["url"] = request.full_url
        captured["headers"] = request.headers
        return _FakeResponse(body.encode("utf-8"))

    monkeypatch.setattr(hibp.urllib.request, "urlopen", fake_urlopen)


def test_pwned_count_hit(monkeypatch):
    captured = {}
    body = f"{SUFFIX}:2817000\r\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA:0\r\n"
    _install_fake_urlopen(monkeypatch, body, captured)

    assert hibp.pwned_count(PASSWORD) == 2817000
    assert hibp.is_pwned(PASSWORD) is True
    # Privacy: only the 5-char prefix leaves the machine.
    assert captured["url"].endswith(f"/range/{PREFIX}")
    assert SUFFIX not in captured["url"]


def test_pwned_count_miss(monkeypatch):
    captured = {}
    body = "1111111111111111111111111111111111A:5\r\n2222222222222222222222222222222222B:9\r\n"
    _install_fake_urlopen(monkeypatch, body, captured)

    assert hibp.pwned_count(PASSWORD) == 0
    assert hibp.is_pwned(PASSWORD) is False


def test_pwned_count_network_error(monkeypatch):
    def boom(request, timeout=None):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(hibp.urllib.request, "urlopen", boom)

    assert hibp.pwned_count(PASSWORD) is None
    assert hibp.is_pwned(PASSWORD) is None


@pytest.mark.network
def test_pwned_count_real_api():
    assert hibp.pwned_count("password") > 0
    assert hibp.pwned_count("a-very-unlikely-passphrase-xq7z-9931-plum") == 0
