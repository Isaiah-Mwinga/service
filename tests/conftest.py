import sys
import os
import pytest
from unittest.mock import patch

# # Ensure the root directory is in the sys path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ.setdefault("AFRICASTALKING_API_KEY", "dummy_api_key")


@pytest.fixture(autouse=True)
def mock_auth():
    """Globally mock authentication for all tests."""
    with patch("app.routes.auth.get_current_user") as mock_user:
        mock_user.return_value = {"sub": "123456", "name": "Test User"}
        yield
