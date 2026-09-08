def has_sequential_pattern(password: str) -> bool:
    for i in range(len(password) - 2):
        chunk = password[i:i+3]
        if _is_ascending(chunk) or _is_descending(chunk) or _is_repeated(chunk):
            return True
    return False


def _is_ascending(chunk: str) -> bool:
    return ord(chunk[1]) == ord(chunk[0]) + 1 and ord(chunk[2]) == ord(chunk[1]) + 1


def _is_descending(chunk: str) -> bool:
    return ord(chunk[1]) == ord(chunk[0]) - 1 and ord(chunk[2]) == ord(chunk[1]) - 1


def _is_repeated(chunk: str) -> bool:
    return chunk[0] == chunk[1] == chunk[2]

KEYBOARD_WALKS = [
    "qwerty",
    "asdfgh",
    "zxcvbn",
    "1qaz",
    "qazwsx",
    "poiuyt",
    "lkjhgf",
    "mnbvcx",
]


def has_keyboard_walk(password: str) -> bool:
    lowered = password.lower()
    for walk in KEYBOARD_WALKS:
        if walk in lowered or walk[::-1] in lowered:
            return True
    return False


def has_weak_pattern(password: str) -> bool:
    return has_sequential_pattern(password) or has_keyboard_walk(password)
