import pytest

from src.blocklist import (
    is_common_password,
    normalize_password,
    reverse_leetspeak,
)


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Password123!", "password"),
        ("hello", "hello"),
        ("admin$$$", "admin"),
        ("letmein2024", "letmein"),
        ("12345", ""),
        ("MixedCASE", "mixedcase"),
    ],
)
def test_normalize_password(raw, expected):
    assert normalize_password(raw) == expected


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("p@ssw0rd", "password"),
        ("h3ll7", "hellt"),
        ("nochange", "nochange"),
        ("$1mple", "simple"),
    ],
)
def test_reverse_leetspeak(raw, expected):
    assert reverse_leetspeak(raw) == expected


@pytest.mark.parametrize("pw", ["password", "123456", "qwerty", "PASSWORD"])
def test_is_common_password_flags_known(pw, common_passwords):
    assert is_common_password(pw, common_passwords) is True


def test_is_common_password_flags_leetspeak(common_passwords):
    assert is_common_password("P@ssw0rd123!", common_passwords) is True


@pytest.mark.parametrize(
    "pw",
    ["xK9$mLp2qR", "correcthorsebatterystaple", "vivid-marmoset-truck-92"],
)
def test_is_common_password_allows_safe(pw, common_passwords):
    assert is_common_password(pw, common_passwords) is False
