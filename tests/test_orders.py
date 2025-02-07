import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.models import Order
from datetime import datetime

client = TestClient(app)


@pytest.fixture
def test_order():
    """Creates a mock test order."""
    return Order(
        id=1,
        customer_id=1,
        item="Laptop",
        amount=1000,
        time=datetime(2025, 2, 5, 12, 0, 0),
    )


@patch("app.crud.create_order")
@patch("app.workers.tasks.send_sms.delay")  # Mock Celery task
def test_create_order(mock_send_sms, mock_create_order):
    """Test creating an order."""
    mock_send_sms.return_value = None
    mock_create_order.return_value = {
        "id": 1,
        "item": "Laptop",
        "amount": 1000,
        "time": "2025-02-05T12:00:00",
        "customer_id": 1,
    }
    response = client.post(
        "/orders/",
        json={
            "customer_id": 1,
            "item": "Laptop",
            "amount": 1000,
            "time": "2025-02-05T12:00:00",
        },
    )
    assert response.status_code == 200
    assert response.json()["item"] == "Laptop"
    assert response.json()["amount"] == 1000


@patch("app.crud.get_orders")
def test_get_orders(mock_get_orders):
    """Test retrieving all orders."""
    mock_get_orders.return_value = [
        {
            "id": 1,
            "customer_id": 1,
            "item": "Laptop",
            "amount": 1000,
            "time": "2025-02-05T12:00:00",
        }
    ]
    response = client.get("/orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["item"] == "Laptop"


@patch("app.crud.get_order")
def test_get_order(mock_get_order):
    """Test retrieving a single order."""
    mock_get_order.return_value = {
        "id": 1,
        "customer_id": 1,
        "item": "Laptop",
        "amount": 1000,
        "time": "2025-02-05T12:00:00",
    }
    response = client.get("/orders/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["item"] == "Laptop"


@patch("app.crud.update_order")
def test_update_order(mock_update_order, test_order):
    """Test updating an order."""
    mock_update_order.return_value = {
        "id": test_order.id,
        "customer_id": test_order.customer_id,
        "item": "Gaming Laptop",
        "amount": test_order.amount,
        "time": test_order.time.isoformat(),
    }
    response = client.put(f"/orders/{test_order.id}", json={"item": "Gaming Laptop"})
    assert response.status_code == 200
    assert response.json()["item"] == "Gaming Laptop"


@patch("app.crud.delete_order")
def test_delete_order(mock_delete_order, test_order):
    """Test deleting an order."""
    mock_delete_order.return_value = {"message": "Order deleted successfully"}
    response = client.delete(f"/orders/{test_order.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Order deleted successfully"}
