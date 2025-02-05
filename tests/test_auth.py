# import pytest
# from fastapi.testclient import TestClient
# from unittest.mock import patch

# def test_login(client: TestClient):
#     """Test OpenID login"""
#     with patch("app.auth.authenticate_user") as mock_auth:
#         mock_auth.return_value = {"access_token": "test_token", "token_type": "bearer"}

#         response = client.post("/auth/token", json={"username": "user", "password": "pass"})
#         assert response.status_code == 200
#         data = response.json()
#         assert "access_token" in data
#         assert data["token_type"] == "bearer"

# def test_invalid_login(client: TestClient):
#     """Test invalid login attempt"""
#     with patch("app.auth.authenticate_user") as mock_auth:
#         mock_auth.return_value = None

#         response = client.post("/auth/token", json={"username": "wrong", "password": "wrong"})
#         assert response.status_code == 401
#         assert response.json()["detail"] == "Invalid credentials"
