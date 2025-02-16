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
@patch("app.workers.tasks.send_sms.delay")  # ✅ Mock existing task
def test_create_order(
    mock_send_sms, mock_create_order, sample_order, sample_order_payload
):
    """Test creating an order."""
    mock_create_order.return_value = sample_order
    mock_send_sms.return_value = "SMS sent successfully"  # Mock response

    response = client.post("/orders/", json=sample_order_payload)

    assert response.status_code == 200
    assert response.json()["item"] == "Laptop"
    assert response.json()["amount"] == 1000
    mock_send_sms.assert_called_once()


@patch("app.crud.get_orders")
def test_get_orders(mock_get_orders, test_order_data):
    """Test retrieving orders using test data from conftest.py."""
    mock_get_orders.return_value = [test_order_data]

    response = client.get("/orders/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["item"] == test_order_data["item"]


@patch("app.crud.get_order")
def test_get_order(mock_get_order, test_order_data):
    """Test retrieving a single order using test data from conftest.py."""
    mock_get_order.return_value = test_order_data

    response = client.get(f"/orders/{test_order_data['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == test_order_data["id"]
    assert response.json()["item"] == test_order_data["item"]


@patch("app.crud.update_order")
def test_update_order(mock_update_order, test_order_data):
    """Test updating an order using test data from conftest.py."""
    updated_data = test_order_data.copy()
    updated_data["item"] = "Updated Laptop"
    updated_data["amount"] = 1200.0

    mock_update_order.return_value = updated_data

    response = client.put(
        f"/orders/{test_order_data['id']}",
        json={"item": "Updated Laptop", "amount": 1200.0},
    )

    assert response.status_code == 200
    assert response.json()["item"] == "Updated Laptop"
    assert response.json()["amount"] == 1200.0


@patch("app.crud.delete_order")
def test_delete_order(mock_delete_order, test_order_data):
    """Test deleting an order using test data from conftest.py."""
    mock_delete_order.return_value = {"detail": "Order deleted successfully"}

    response = client.delete(f"/orders/{test_order_data['id']}")

    assert response.status_code == 200
    assert response.json() == {"message": "Order deleted successfully"}
