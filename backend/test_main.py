from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_hello_endpoint():
    """Test du endpoint /api/hello"""
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "La connexion avec l'API est réussie, amusez-vous bien sur ENSAI TCG !"}

def test_routes_exist():
    """Vérifie que les routes essentielles existent"""
    existing_routes = {route.path for route in app.routes}
    expected_routes = {"/api/hello", "/auth", "/cards", "/booster", "/proxy"}

    # Vérifie que toutes les routes attendues sont bien présentes
    assert expected_routes.issubset(existing_routes)
