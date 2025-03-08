from fastapi.testclient import TestClient
from backend.main import app
from backend.app.models.user_model import User
from backend.app.db.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

# Configuration pour utiliser une base de données en mémoire pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Création du moteur de base de données pour les tests
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer les tables nécessaires pour les tests
@pytest.fixture(scope="module")
def db_session():
    # Créer les tables
    from backend.app.db.database import Base
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialiser le client TestClient pour envoyer des requêtes
@pytest.fixture(scope="module")
def client():
    client = TestClient(app)
    return client

# Créer un utilisateur de test
@pytest.fixture(scope="module")
def test_user(db_session):
    user = User(username="testuser", password="testpassword", e_mail="testuser@example.com", role="USER")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def test_create_access_token(client, test_user):
    # Effectuer une requête POST sur /auth/token pour obtenir un jeton JWT
    response = client.post(
        "/auth/token", data={"username": test_user.username, "password": "testpassword"}
    )
    print("Response status:", response.status_code)
    print("Response JSON:", response.json()) 
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()

