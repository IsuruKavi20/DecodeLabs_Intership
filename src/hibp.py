

import hashlib
import urllib.error
import urllib.request

PWNED_RANGE_URL = "https://api.pwnedpasswords.com/range/{prefix}"
_USER_AGENT = "password-strength-checker"


def pwned_count(password: str, *, timeout: float = 4.0) -> int | None:
    """Return how many times `password` appears in the HIBP breach corpus.

    Returns 0 if it is not present, and None if the API could not be reached
    (offline, timeout, HTTP error). None means "unknown", not "safe".
    """
    digest = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = digest[:5], digest[5:]

    request = urllib.request.Request(
        PWNED_RANGE_URL.format(prefix=prefix),
        headers={"User-Agent": _USER_AGENT, "Add-Padding": "true"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError, OSError):
        return None

    for line in body.splitlines():
        candidate, _, count = line.partition(":")
        if candidate.strip().upper() == suffix:
            try:
                return int(count.strip())
            except ValueError:
                return None
    return 0


def is_pwned(password: str, **kwargs) -> bool | None:
    """True/False if the breach status is known, None if the check was unavailable."""
    count = pwned_count(password, **kwargs)
    if count is None:
        return None
    return count > 0
