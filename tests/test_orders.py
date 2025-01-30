# tests/test_orders.py
import os
import sys
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Ensure the app directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

client = TestClient(app)

def test_create_order():
    response = client.post("/orders/", json={"item": "Laptop", "amount": 1500, "customer_id": 1})
    assert response.status_code == 200
    assert response.json()["item"] == "Laptop"

def test_read_orders():
    response = client.get("/orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)