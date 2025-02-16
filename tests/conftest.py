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


@pytest.fixture
def test_customer_data():
    return {
        "name": "John Doe",
        "code": "JD123",
        "phone_number": "+254712345678",
    }


@pytest.fixture
def test_order_data():
    """Fixture for test order data."""
    return {
        "id": 1,
        "customer_id": 1,
        "item": "Laptop",
        "amount": 1000,
        "time": "2025-02-05T12:00:00",
    }


@pytest.fixture
def sample_order():
    """Fixture for a sample order."""
    return {
        "id": 1,
        "customer_id": 1,
        "item": "Laptop",
        "amount": 1000,
        "time": "2025-02-05T12:00:00",
    }


@pytest.fixture
def sample_order_payload():
    """Fixture for creating an order (without ID)."""
    return {
        "customer_id": 1,
        "item": "Laptop",
        "amount": 1000,
        "time": "2025-02-05T12:00:00",
    }
