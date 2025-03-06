"""
Ce module contient des services pour la gestion des cartes dans l'application.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.app.models.Card import Card, CardBase
from backend.app.models.Enums import Role


async def get_cards(skip: int, limit: int, db: Session):
    """
    Récupère les cartes avec pagination.

    Args:
        skip (int): Le nombre de cartes à ignorer pour la pagination.
        limit (int): Le nombre maximum de cartes à récupérer.
        db (Session): La session de base de données.

    Returns:
        list: La liste des cartes récupérées.
    """
    cards = db.query(Card).offset(skip).limit(limit).all()
    return cards

async def add_card(card_data: CardBase, db: Session, current_user: dict):
    """
    Ajoute une nouvelle carte dans la base de données.

    Args:
        card_data (CardBase): Les données de la carte à ajouter.
        db (Session): La session de base de données.
        current_user (dict): Les informations de l'utilisateur actuel.

    Returns:
        dict: Message de succès et détails de la carte ajoutée.

    Raises:
        HTTPException: Si l'utilisateur n'a pas le rôle d'administrateur.
    """
    if current_user["role"] != Role.ADMIN:
        raise HTTPException(status_code=403,
                            detail="Accès interdit : Vous devez être administrateur pour ajouter des cartes") 
    new_card = Card(name=card_data.name, image_url=card_data.image_url, rarity=card_data.rarity)
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return {"message": "Carte ajoutée avec succès", "card": new_card}
