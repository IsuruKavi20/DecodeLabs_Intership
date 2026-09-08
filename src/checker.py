

try:
    from .blocklist import is_common_password
    from .patterns import has_weak_pattern
    from .hibp import pwned_count
except ImportError:  # running as a plain script rather than a package
    from blocklist import is_common_password
    from patterns import has_weak_pattern
    from hibp import pwned_count

MIN_LENGTH = 8


def _length_bonus(length: int) -> tuple[int, str]:
    if length >= 20:
        return 4, "Excellent length (20+ chars)"
    if length >= 16:
        return 3, "Great length (16-19 chars)"
    if length >= 12:
        return 2, "Good length (12-15 chars)"
    return 1, "Acceptable length (8-11 chars)"


def check_password_strength(
    password: str,
    common_passwords: set[str],
    *,
    online_check: bool = False,
) -> dict:
    reasons: list[str] = []

    # --- Gates: any of these means "Weak", no scoring ---
    if len(password) < MIN_LENGTH:
        reasons.append(f"Too short (minimum {MIN_LENGTH} characters)")
        return {"score": 0, "strength": "Weak", "reasons": reasons}

    if is_common_password(password, common_passwords):
        reasons.append("Found in common / breached password list")
        return {"score": 0, "strength": "Weak", "reasons": reasons}

    online_note: str | None = None
    if online_check:
        count = pwned_count(password)
        if count is None:
            online_note = "Note: online breach check was unavailable; used local list only"
        elif count > 0:
            reasons.append(
                f"Seen {count:,} times in the Have I Been Pwned breach corpus"
            )
            return {"score": 0, "strength": "Weak", "reasons": reasons}
        else:
            reasons.append("Not found in the Have I Been Pwned breach corpus")

    # --- Scoring ---
    score, length_reason = _length_bonus(len(password))
    reasons.append(length_reason)
    if len(password) < 12:
        reasons.append("Consider a longer password or passphrase")

    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    if has_upper:
        score += 1
        reasons.append("Contains an uppercase letter")
    else:
        reasons.append("Missing an uppercase letter")

    if has_digit:
        score += 1
        reasons.append("Contains a digit")
    else:
        reasons.append("Missing a digit")

    if has_symbol:
        score += 1
        reasons.append("Contains a symbol")
    else:
        reasons.append("Missing a symbol")

    if has_weak_pattern(password):
        score -= 2
        reasons.append(
            "Contains a predictable pattern (sequence, repeat, or keyboard walk)"
        )

    # --- Classification ---
    if score <= 2:
        strength = "Weak"
    elif score == 3:
        strength = "Medium"
    else:
        strength = "Strong"

    
    class_count = sum((has_upper, has_digit, has_symbol))
    if strength == "Strong" and len(password) < 16 and class_count < 2:
        strength = "Medium"
        reasons.append(
            "Short passwords need more character variety (mix upper/lower/digits/"
            "symbols) or more length to rate Strong"
        )

    if online_note:
        reasons.append(online_note)

    return {"score": score, "strength": strength, "reasons": reasons}
