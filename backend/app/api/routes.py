from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Column, String
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.models.User import User, UserBase

router = APIRouter()

##Routes User
@router.get("/check-db-connection/")
def check_db_connection(db: Session = Depends(get_db)):
    try:
        # Essayer de faire une requête simple pour vérifier la connexion
        db.execute("SELECT 1")
        return {"message": "Connexion à la base de données réussie !"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de connexion à la base de données : {str(e)}")
    
@router.post("/nouvelle_utilisateur/")
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        password=user.password,
        role=user.role,
        e_mail=user.e_mail
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "Utilisateur créé avec succès", "user": db_user}

##Routes Card
from backend.app.models.Card import Card, CardBase


@router.post("/cards/")
async def create_card(card: CardBase, db: Session = Depends(get_db)):
    db_card = Card(
        name=card.name,
        image_url=card.image_url,
        rarity=card.rarity
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return {"message": "Carte créée avec succès", "card": db_card}

@router.get("/cards/")
async def read_cards(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cards = db.query(Card).offset(skip).limit(limit).all()
    return cards


##Routes Collection
from backend.app.models.Collection import Collection, CollectionBase


@router.post("/collections/")
async def create_collection(collection: CollectionBase, db: Session = Depends(get_db)):
    db_collection = Collection(name=collection.name)
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return {"message": "Collection créée avec succès", "collection": db_collection}

@router.get("/collections/")
async def read_collections(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    collections = db.query(Collection).offset(skip).limit(limit).all()
    return collections


##Routes Booster

from backend.app.services.BoosterService import BoosterService


#ouvrir booster
@router.post("/open_booster/")
async def open_booster(user_id: str, collection_id: int, db: Session = Depends(get_db)):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    try:
        cards = BoosterService.open_booster(user_id, collection, db=db)
        return {"cards": cards}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


# Soumission/Approbation/Rejet des cartes

@router.post("/collections/{collection_id}/cards/")
async def add_card_to_collection(collection_id: int, name: str, image_url: str, rarity: str, db: Session = Depends(get_db)):
    db_card = Card(
        name=name,
        image_url=image_url,
        rarity=rarity,
        collection_id=collection_id
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return {"message": "Carte ajoutée avec succès", "card": db_card}

@router.put("/cards/{card_id}/approve/")
async def approve_card(card_id: int, db: Session = Depends(get_db)):
    db_card = db.query(Card).filter(Card.id == card_id).first()
    if not db_card:
        raise HTTPException(status_code=404, detail="Carte non trouvée")

    db_card.is_approved = True
    db.commit()
    db.refresh(db_card)
    return {"message": "Carte approuvée avec succès", "card": db_card}

@router.delete("/cards/{card_id}/reject/")
async def reject_card(card_id: int, db: Session = Depends(get_db)):
    db_card = db.query(Card).filter(Card.id == card_id).first()
    if not db_card:
        raise HTTPException(status_code=404, detail="Carte non trouvée")

    db.delete(db_card)
    db.commit()
    return {"message": "Carte rejetée avec succès"}
