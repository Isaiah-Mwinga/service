# tests/test_customers.py
import os
import sys
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Ensure the app directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
client = TestClient(app)

def test_create_customer():
    response = client.post("/customers/", json={"name": "John Doe", "code": "JD123"})
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"

def test_read_customers():
    response = client.get("/customers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

