import os
import re
import pytest

MONOLITHIC_PATTERN = re.compile(r"^GMRTI_\d+\.md$")


@pytest.fixture(scope="session")
def base_dir():
    """Returns the absolute path to the repository root directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
