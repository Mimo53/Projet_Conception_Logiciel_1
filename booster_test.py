import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from backend.main import app  # Remplace par le bon chemin vers ton app
from backend.app.api.routes.booster import open_booster_service

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_user():
    return {"id": 1, "username": "testuser"}

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_open_booster_service():
    return AsyncMock(return_value={"message": "Booster opened", "cards": ["card1", "card2"]})

def test_open_booster(client, mock_user, mock_db, mock_open_booster_service, monkeypatch):
    # Mock des dépendances
    monkeypatch.setattr("backend.app.routers.booster.get_current_user", lambda: mock_user)
    monkeypatch.setattr("backend.app.routers.booster.get_db", lambda: mock_db)
    monkeypatch.setattr("backend.app.routers.booster.open_booster_service", mock_open_booster_service)

    # Envoi d'une requête POST à l'endpoint
    response = client.post("/open_booster_and_add/")

    # Vérification des résultats
    assert response.status_code == 200
    assert response.json() == {"message": "Booster opened", "cards": ["card1", "card2"]}
    mock_open_booster_service.assert_awaited_once_with(mock_user, mock_db)
