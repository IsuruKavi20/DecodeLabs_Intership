"""Interactive command-line entry point for the password strength checker.

Run from the repository root:  python -m src.main
"""

import sys
# getpass reads the password without echoing it to the terminal. For a security
# tool this matters: an echoed password lands in the terminal scrollback, in
# screen-sharing/recordings, and in plain view of anyone looking at the screen.
from getpass import getpass

try:
    from .blocklist import load_common_passwords
    from .checker import check_password_strength
except ImportError:  # running as `python src/main.py` rather than `-m src.main`
    from blocklist import load_common_passwords
    from checker import check_password_strength

DATA_FILE = "data/common_passwords.txt"
QUIT_WORD = "exit"


def _ask_online_check() -> bool:
    answer = input(
        "Enable online breach check via Have I Been Pwned? Only the first 5 chars "
        "of your password's SHA-1 hash are sent (k-anonymity). [y/N]: "
    ).strip().lower()
    return answer in {"y", "yes"}


def _print_result(result: dict) -> None:
    print()
    print(f"  Strength: {result['strength']}  (score {result['score']})")
    print("  Reasons:")
    for reason in result["reasons"]:
        print(f"    - {reason}")
    print()


def main() -> int:
    try:
        common_passwords = load_common_passwords(DATA_FILE)
    except FileNotFoundError:
        print(
            f"Could not find '{DATA_FILE}'. Run this from the repository root.",
            file=sys.stderr,
        )
        return 1

    print(f"Password Strength Checker  (type '{QUIT_WORD}' to quit)")
    online_check = _ask_online_check()

    while True:
        try:
            password = getpass("Enter a password to check (or 'exit' to quit): ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if password.strip().lower() == QUIT_WORD:
            break
        if not password:
            print("  (empty input - try again)")
            continue

        result = check_password_strength(
            password, common_passwords, online_check=online_check
        )
        _print_result(result)

    print("Bye.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
