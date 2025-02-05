from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)

@patch("app.dependencies.get_db")
@patch("app.workers.tasks.send_sms.delay")
def test_create_order(mock_send_sms, mock_get_db):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    
    mock_customer = MagicMock()
    mock_customer.id = 1
    mock_customer.name = "John Doe"
    mock_customer.phone_number = "1234567890"
    mock_db.query().filter_by().first.return_value = mock_customer
    
    mock_order = schemas.Order(id=1, item="Laptop", amount=1000, time="2025-02-05T12:00:00", customer=mock_customer)
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    mock_db.query().filter().first.return_value = mock_order
    
    response = client.post("/orders/", json={
        "item": "Laptop",
        "amount": 1000,
        "time": "2025-02-05T12:00:00",
        "customer_id": 1
    })
    
    assert response.status_code == 200
    assert response.json()["item"] == "Laptop"
    mock_send_sms.assert_called()

def test_get_orders():
    with patch("app.dependencies.get_db") as mock_get_db:
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        
        mock_order = schemas.Order(id=1, item="Laptop", amount=1000, time="2025-02-05T12:00:00", customer=MagicMock())
        mock_db.query().all.return_value = [mock_order]
        
        response = client.get("/orders/")
        
        assert response.status_code == 200
        assert len(response.json()) == 1

def test_update_order():
    with patch("app.dependencies.get_db") as mock_get_db:
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        
        mock_order = MagicMock()
        mock_db.query().filter().first.return_value = mock_order
        
        response = client.put("/orders/1", json={"item": "Phone", "amount": 500})
        
        assert response.status_code == 200
        mock_db.commit.assert_called()

def test_delete_order():
    with patch("app.dependencies.get_db") as mock_get_db:
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        
        mock_order = MagicMock()
        mock_db.query().filter().first.return_value = mock_order
        
        response = client.delete("/orders/1")
        
        assert response.status_code == 200
        assert response.json() == {"message": "Order deleted successfully"}
        mock_db.commit.assert_called()
