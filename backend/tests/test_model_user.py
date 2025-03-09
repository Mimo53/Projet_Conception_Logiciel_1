"""
Test pour la connection des utilisateurs
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.db.database import Base, engine
from backend.app.models.user_model import User
from backend.app.models.enums import Role
from backend.app.models.user_card import UserCard
from backend.app.models.card_model import Card

# Configuration pour une base de données SQLite en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer les tables nécessaires pour les tests
@pytest.fixture(scope="module")
def db_session():
    """Fixture pour créer une session de test"""
    # Créer les tables
    Base.metadata.create_all(bind=engine)

    # Créer une session
    db = SessionLocal()
    yield db  # Donne accès à la session aux tests
    db.close()

# Supprimer l'utilisateur si déjà présent avant d'ajouter un nouvel utilisateur
@pytest.fixture(scope="module")
def prepare_user(db_session):
    """Supprime l'utilisateur existant (si nécessaire) et prépare un utilisateur pour le test"""
    # Supprimer l'utilisateur s'il existe
    existing_user = db_session.query(User).filter(User.username == "test_user").first()
    if existing_user:
        db_session.delete(existing_user)
        db_session.commit()

    # Créer un nouvel utilisateur
    new_user = User(
        username="test_user",
        password="test_password",
        role=Role.USER,
        e_mail="test@example.com"
    )
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    return new_user

# Test de création d'un utilisateur dans la base de données
def test_create_user(db_session, prepare_user):
    """Test de création d'un utilisateur dans la base de données"""
    # Assurer que l'utilisateur est bien préparé
    db_user = db_session.query(User).filter(User.username == "test_user").first()

    print(db_user)  # Pour vérifier si l'utilisateur est bien inséré

    # Vérifie que l'utilisateur a bien été inséré
    assert db_user is not None
    assert db_user.username == "test_user"
    assert db_user.e_mail == "test@example.com"
    assert db_user.role == Role.USER

# Test de mise à jour d'un utilisateur
def test_user_update(db_session, prepare_user):
    """Test de mise à jour d'un utilisateur"""
    # Récupérer l'utilisateur existant
    user = db_session.query(User).filter(User.username == "test_user").first()

    # Vérifie que l'utilisateur existe avant de faire la mise à jour
    assert user is not None  # Assure-toi que l'utilisateur existe

    # Mise à jour de l'email
    user.e_mail = "new_email@example.com"
    db_session.commit()

    # Vérifie que l'email a bien été mis à jour
    updated_user = db_session.query(User).filter(User.username == "test_user").first()
    assert updated_user.e_mail == "new_email@example.com"
