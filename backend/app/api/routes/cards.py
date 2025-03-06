"""
Module des routes des cartes pour l'API.

Ce module contient les routes pour récupérer les cartes et créer une nouvelle carte 
pour un utilisateur dans le système.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.services.card_service import add_card, get_cards
from backend.app.core.security import get_current_user
from backend.app.db.database import get_db
from backend.app.models.Card import CardBase
router = APIRouter(prefix='/cards', tags=['cards'])

@router.get("/")
async def read_cards(skip: int = 0,
                    limit: int = 10,
                    db: Session = Depends(get_db)):
    """
    Récupère une liste de cartes à partir de la base de données.

    Args:
        skip (int): Le nombre de cartes à ignorer pour la pagination (par défaut 0).
        limit (int): Le nombre maximal de cartes à récupérer (par défaut 10).
        db (Session): La session de base de données.

    Returns:
        list: Liste des cartes récupérées.
    """
    return await get_cards(skip, limit, db)

@router.post("/")
async def create_card(card_data: CardBase,
                    db: Session = Depends(get_db),
                    current_user: dict = Depends(get_current_user)):
    """
    Crée une nouvelle carte et l'ajoute à la base de données.

    Args:
        card_data (CardBase): Les données de la carte à créer.
        db (Session): La session de base de données.
        current_user (dict): L'utilisateur actuel.

    Returns:
        dict: Les informations sur la carte créée.
    """
    return await add_card(card_data, db, current_user)
