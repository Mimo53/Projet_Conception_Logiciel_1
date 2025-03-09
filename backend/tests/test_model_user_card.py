"""
Test card pour voir la relation entre cartes et utilisateurs
"""

from backend.app.models.user_card import UserCard
from backend.app.models.card_model import Card
from backend.app.models.user_model import User
from backend.app.models.enums import Role,Rarity
from backend.tests.test_model_user import db_session

import pytest

@pytest.fixture(scope="module")
def create_user_and_card(db_session):
    """Fixture pour créer un utilisateur et une carte de test"""
    # Vérifier si l'utilisateur existe déjà pour éviter le conflit UNIQUE
    user = db_session.query(User).filter(User.username == "test_user").first()
    if not user:
        user = User(
            username="test_user",
            password="test_password",
            role=Role.USER,
            e_mail="test@example.com"
        )
        db_session.add(user)
        db_session.commit()

    card = db_session.query(Card).filter(Card.id == 1).first()
    if not card:
        card = Card(id=1, name="Test Card", image_url="http://example.com", rarity="LEGENDAIRE")
        db_session.add(card)
        db_session.commit()

    user_card = db_session.query(UserCard).filter(UserCard.user_id == user.username, UserCard.card_id == card.id).first()
    if not user_card:
        user_card = UserCard(user_id=user.username, card_id=card.id, obtained=True)
        db_session.add(user_card)
        db_session.commit()

    return user, card, user_card


def test_user_card_relationship(create_user_and_card, db_session):
    """Test de la relation entre un utilisateur et une carte"""
    user, card, user_card = create_user_and_card

    # Vérifie que la liaison utilisateur-carte existe
    user_card = db_session.query(UserCard).filter(UserCard.user_id == "test_user").first()
    assert user_card is not None
    assert user_card.user_id == "test_user"
    assert user_card.card_id == 1
    assert user_card.obtained is True
