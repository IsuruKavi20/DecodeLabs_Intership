from pathlib import Path

LEET_MAP = {
    "@": "a",
    "0": "o",
    "3": "e",
    "1": "i",
    "$": "s",
    "7": "t",
}
_LEET_TRANSLATION = str.maketrans(LEET_MAP)


def load_common_passwords(filepath: str = "data/common_passwords.txt") -> set[str]:
    path = Path(filepath)
    with path.open("r", encoding="utf-8") as file:
        return {line.strip().lower() for line in file}

def normalize_password(password: str) -> str:
    result = password.lower()
    while result and (result[-1].isdigit() or not result[-1].isalnum()):
        result = result[:-1]
    return result


def reverse_leetspeak(password: str) -> str:
    """Undo common leetspeak substitutions, e.g. "P@ssw0rd" -> "password"."""
    return password.lower().translate(_LEET_TRANSLATION)


def is_common_password(password: str, common_passwords: set[str]) -> bool:
    
    candidates = {
        password.lower(),
        normalize_password(password),
        reverse_leetspeak(password),
        normalize_password(reverse_leetspeak(password)),
    }
    return any(candidate in common_passwords for candidate in candidates)