from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.routes.auth import get_current_user

# Test client
client = TestClient(app)

# Mock authentication function
def override_get_current_user():
    return {"sub": "123456", "name": "Test User"}

# Override FastAPI dependency
app.dependency_overrides[get_current_user] = override_get_current_user


@patch("app.crud.create_order")
def test_create_order(mock_create_order):
    """Test creating an order."""
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
    """Test retrieving orders."""
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
def test_update_order(mock_update_order):
    """Test updating an order."""
    mock_update_order.return_value = {
        "id": 1,
        "customer_id": 1,
        "item": "Updated Laptop",
        "amount": 1200.0,
        "time": "2025-02-05T12:00:00",  # Add this field
    }
    response = client.put(
        "/orders/1",
        json={"item": "Updated Laptop", "amount": 1200.0},
    )
    assert response.status_code == 200
    assert response.json()["item"] == "Updated Laptop"

@patch("app.crud.delete_order")
def test_delete_order(mock_delete_order):
    """Test deleting an order."""
    mock_delete_order.return_value = {"detail": "Order deleted successfully"}
    response = client.delete("/orders/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Order deleted successfully"}