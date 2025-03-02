from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.app.models.Card import Card, CardBase
from backend.app.models.Enums import Role


async def get_cards(skip: int, limit: int, db: Session):
    cards = db.query(Card).offset(skip).limit(limit).all()
    return cards

async def add_card(card_data: CardBase, db: Session, current_user: dict):
    if current_user["role"] != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Accès interdit : Vous devez être administrateur pour ajouter des cartes")
    new_card = Card(name=card_data.name, image_url=card_data.image_url, rarity=card_data.rarity)
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return {"message": "Carte ajoutée avec succès", "card": new_card}
