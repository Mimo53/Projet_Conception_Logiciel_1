"""
Ce module contient des services pour la gestion des boosters dans l'application.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.app.models.Booster import BoosterBuilder
from backend.app.models.Card import Card
from backend.app.models.UserCard import UserCard

async def open_booster_and_add(user: dict, db: Session):
    """
    Ouvre un booster et ajoute les cartes à la collection de l'utilisateur.

    Args:
        user (dict): Dictionnaire contenant les informations de l'utilisateur.
        db (Session): Instance de la session de base de données.

    Returns:
        dict: Réponse contenant le message et la liste des cartes ajoutées.
    """
    try:
        print(f"📩 Requête reçue pour ouvrir un booster par {user['username']}")
        user_id = user["username"]
        builder = BoosterBuilder(db)
        cards = builder.with_random_cards().build()
        user_cards = []

        for card in cards:
            user_card = UserCard(user_id=user_id, card_id=card.id, obtained=True)
            db.add(user_card)
            user_cards.append({
                "id": card.id,
                "name": card.name,
                "image_url": card.image_url,
                "rarity": card.rarity.name
            })

        db.commit()
        print(f"Booster ouvert avec {len(cards)} cartes ajoutées.")
        return {"message": "Booster ouvert et cartes ajoutées.", "cards": user_cards}

    except Exception as e:
        print(f"❌ Erreur dans open_booster_and_add: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur") from e


async def view_collection(user: dict, db: Session):
    """
    Consulte la collection de cartes d'un utilisateur.

    Args:
        user (dict): Dictionnaire contenant les informations de l'utilisateur.
        db (Session): Instance de la session de base de données.

    Returns:
        dict: La collection de cartes de l'utilisateur.
    """
    try:
        print(f"Consultation de la collection pour {user['username']}")
        user_id = user["username"]
        user_cards = (db.query(UserCard)
                        .join(Card, UserCard.card_id == Card.id)
                        .filter(UserCard.user_id == user_id, UserCard.obtained is True)
                        .all())

        if not user_cards:
            raise HTTPException(status_code=404,
                                detail="Aucune carte trouvée pour cet utilisateur.")

        collection = [{
            "card_name": user_card.card.name,
            "image_url": user_card.card.image_url,
            "rarity": user_card.card.rarity.name
        } for user_card in user_cards]

        print(f"💼 Collection de {user_id} contient {len(collection)} cartes.")
        return {"user_id": user_id, "collection": collection}

    except Exception as e:
        print(f"❌ Erreur dans view_collection: {e}")
        raise HTTPException(status_code=500,detail="Erreur serveur") from e
