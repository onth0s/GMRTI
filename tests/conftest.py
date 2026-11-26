import os
import pytest

from _gmrti_common import MONOLITHIC_PATTERN


@pytest.fixture(scope="session")
def base_dir():
    """Returns the absolute path to the repository root directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
