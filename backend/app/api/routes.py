from typing import List

from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy import Column, String
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.models.User import User, UserBase, UserUpdate
from sqlalchemy import text


# Instancier un contexte pour le hachage du mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

router = APIRouter()

##Routes User
@router.get("/check-db-connection/")
def check_db_connection(db: Session = Depends(get_db)):
    try:
        # Utilisation de text() pour exécuter une requête SQL brute
        db.execute(text("SELECT 1"))
        return {"message": "Connexion à la base de données réussie !"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de connexion à la base de données : {str(e)}")


@router.post("/new_users/")
def create_user(user: UserBase, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="L'utilisateur existe déjà")

    # Création d'un nouvel utilisateur
    db_user = User(
        username=user.username,
        password=hash_password(user.password),  # Assure-toi que cette fonction existe
        role=user.role,
        e_mail=user.e_mail,
        user_cards=[]  # Initialisation de la relation
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "Utilisateur créé avec succès", "user": db_user}

@router.put("/update_user/{username}")  
async def update_user(username: str, update_data: UserUpdate, db: Session = Depends(get_db)):
    # Recherche l'utilisateur dans la base de données
    db_user = db.query(User).filter(User.username == username).first()
    print(db.query(User).all())  # Vérifie tous les utilisateurs présents

    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Vérification si un nouvel username est fourni et s'il est déjà pris
    if update_data.new_username:
        existing_user = db.query(User).filter(User.username == update_data.new_username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Ce nom d'utilisateur est déjà pris")
        db_user.username = update_data.new_username

    # Vérification et mise à jour du mot de passe (haché)
    if update_data.new_password:
        db_user.password = hash_password(update_data.new_password)

    # Sauvegarde des changements
    db.commit()
    db.refresh(db_user)
    
    return {"message": "Utilisateur mis à jour avec succès"}

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

#Route obtention de carte
from backend.app.models.UserCard import UserCard, UserCardBase


@router.post("/users/{user_id}/cards/{card_id}/obtain/", response_model=UserCardBase)
async def obtain_card(user_id: int, card_id: int, db: Session = Depends(get_db)):
    user_card = db.query(UserCard).filter(UserCard.user_id == user_id, UserCard.card_id == card_id).first()
    if not user_card:
        user_card = UserCard(user_id=user_id, card_id=card_id, obtained=True)
        db.add(user_card)
    else:
        user_card.obtained = True
    db.commit()
    db.refresh(user_card)
    return user_card

#Endpoint collection d'un utilisateur
@router.get("/users/{user_id}/obtained_cards/", response_model=List[UserCardBase])
async def get_user_obtained_cards(user_id: int, db: Session = Depends(get_db)):
    user_cards = db.query(UserCard).filter(UserCard.user_id == user_id, UserCard.obtained == True).all()
    return user_cards
