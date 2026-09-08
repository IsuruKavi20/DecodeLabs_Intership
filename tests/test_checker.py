import pytest

from src.checker import check_password_strength


def check(pw, common_passwords):
    return check_password_strength(pw, common_passwords)


# --- Gate 1: length ---
def test_gate_too_short(common_passwords):
    result = check("Ab1$xy", common_passwords)
    assert result["strength"] == "Weak"
    assert any("Too short" in r for r in result["reasons"])


def test_gate_too_short_skips_scoring(common_passwords):
    result = check("aB3$", common_passwords)
    assert result["score"] == 0
    assert len(result["reasons"]) == 1


# --- Gate 2: common / breached list ---
@pytest.mark.parametrize("pw", ["password", "iloveyou", "Password123!"])
def test_gate_common_password(pw, common_passwords):
    result = check(pw, common_passwords)
    assert result["strength"] == "Weak"
    assert any("common" in r.lower() for r in result["reasons"])


# --- Scoring / classification ---
@pytest.mark.parametrize(
    "pw, expected",
    [
        ("correcthorsebatterystaple", "Strong"),   # long lowercase passphrase
        ("MyDog$Fluffy2024", "Strong"),             # 16 chars + all classes
        ("Tr0ub4dor&3", "Strong"),                  # short but 3 classes (borderline)
        ("summerrain12", "Medium"),                 # 12 chars, one digit
        ("abcdefgh", "Weak"),                       # pattern penalty
        ("sunshine", "Weak"),                       # 8 lowercase, no variety
    ],
)
def test_classification(pw, expected, common_passwords):
    assert check(pw, common_passwords)["strength"] == expected


def test_short_lowercase_never_strong(common_passwords):
    # Anything under 16 chars needs real character variety; length alone caps at Medium.
    for pw in ["planetearth", "greenmountain", "quietrivers12"]:
        assert check(pw, common_passwords)["strength"] in {"Weak", "Medium"}


def test_reasons_are_actionable(common_passwords):
    result = check("MyDog$Fluffy2024", common_passwords)
    joined = " ".join(result["reasons"]).lower()
    assert "length" in joined
    assert "uppercase" in joined and "digit" in joined and "symbol" in joined

    missing = check("Longpassword1234", common_passwords)
    assert any("Missing a symbol" == r for r in missing["reasons"])


def test_online_check_disabled_by_default(common_passwords):
    # No network access should be attempted; a fresh string scores normally.
    result = check("vivid-marmoset-truck-92", common_passwords)
    assert result["strength"] in {"Weak", "Medium", "Strong"}
    assert not any("Have I Been Pwned" in r for r in result["reasons"])
