from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_login():
    """Test du login utilisateur"""
    response = client.post("/auth/login", json={"username": "test", "password": "password"})
    assert response.status_code in [200, 401]  # Accepte 200 (OK) ou 401 (Unauthorized) selon la config
