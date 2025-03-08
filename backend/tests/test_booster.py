import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from backend.app.api.services.booster_service import open_booster_and_add
from backend.app.models.card_model import Card
from backend.app.models.user_card import UserCard
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_open_booster_success():
    """Test d'ouverture de booster avec au moins 5 cartes disponibles."""
    mock_user = {"id": 1, "username": "test_user"}
    mock_db = MagicMock()

    # Simuler la construction d'un booster avec 5 cartes avec une rareté définie
    mock_cards = [
        Card(id=i, name=f"Card{i}", image_url=f"url{i}", rarity=MagicMock())
        for i in range(1, 6)  # 5 cartes
    ]

    # Assigner explicitement la valeur "Common" à rarity.name
    for card in mock_cards:
        card.rarity.name = "Common"

    with patch("backend.app.models.booster_model.BoosterBuilder.with_random_cards", return_value=MagicMock(build=MagicMock(return_value=mock_cards))):
        result = await open_booster_and_add(mock_user, mock_db)

    assert result["message"] == "Booster ouvert et cartes ajoutées."
    assert len(result["cards"]) == 5
    for i, card in enumerate(result["cards"]):
        assert card["id"] == i + 1
        assert card["name"] == f"Card{i+1}"
        assert card["image_url"] == f"url{i+1}"
        assert card["rarity"] == "Common"  # Maintenant, la valeur est bien une chaîne



@pytest.mark.asyncio
async def test_open_booster_not_enough_cards():
    """Test d'échec si le booster contient moins de 5 cartes."""
    mock_user = {"id": 1, "username": "test_user"}
    mock_db = MagicMock()

    # Simuler un booster contenant seulement 3 cartes
    mock_cards = [
        Card(id=i, name=f"Card{i}", image_url=f"url{i}", rarity=MagicMock(name="Common"))
        for i in range(1, 4)  # Seulement 3 cartes
    ]

    with patch("backend.app.models.booster_model.BoosterBuilder.with_random_cards", return_value=MagicMock(build=MagicMock(return_value=mock_cards))):
        with pytest.raises(Exception, match="Erreur serveur"):  # Erreur 500 attendue
            await open_booster_and_add(mock_user, mock_db)
