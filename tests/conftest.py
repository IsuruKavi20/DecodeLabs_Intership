import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.blocklist import load_common_passwords  # noqa: E402


@pytest.fixture(scope="session")
def common_passwords() -> set[str]:
    return load_common_passwords(str(REPO_ROOT / "data" / "common_passwords.txt"))
