from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from passlib.context import CryptContext
from sqlalchemy import Column, String
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from backend.app.db.database import get_db
from backend.app.models.User import User, UserBase, UserUpdate
from backend.app.models.UserCard import UserCard, UserCardBase
from starlette import status
from fastapi_mail import FastMail, MessageSchema
from backend.app.models.mail import conf

# Configuration du JWT
SECRET_KEY = "ma_super_cle_secrete"  # Change en production !
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Expiration du token après 30 minutes

# Instancier un contexte pour le hachage du mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()
router_auth = APIRouter(
    prefix='/auth',
    tags=['auth']
)

class Token(BaseModel):
    access_token: str
    token_type: str


# Fonction pour vérifier le mot de passe
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Fonction pour hacher le mot de passe
def hash_password(password: str):
    return pwd_context.hash(password)

# Fonction pour créer un token JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Fonction pour authentifier un utilisateur
def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        return None
    return user


# Route pour créer un utilisateur
@router_auth.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: Session = Depends(get_db), background_tasks: BackgroundTasks = BackgroundTasks()):
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="L'utilisateur existe déjà")

    # Créer l'utilisateur
    db_user = User(
        username=user.username,
        password=hash_password(user.password),
        role=user.role,
        e_mail=user.e_mail,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Envoyer l'e-mail de vérification en arrière-plan
    if db_user.e_mail:
        background_tasks.add_task(send_verification_email, db_user.e_mail, db_user.username)

    return {"message": "Utilisateur créé avec succès, vérifiez votre e-mail", "user": db_user}

async def send_verification_email(email: str, username: str):
    verification_link = f"http://localhost:8000/verify-email/{username}"  # Lien de vérification

    message = MessageSchema(
        subject="Vérification de votre compte",
        recipients=[email],  # Destinataire
        body=f"""
        Bonjour {username},

        Merci de vous être inscrit sur notre plateforme !
        Veuillez cliquer sur le lien suivant pour vérifier votre adresse e-mail :

        {verification_link}

        Cordialement,
        L'équipe de support.
        """,
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

@router_auth.get("/verify-email/{username}")
async def verify_email(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Ici, tu pourrais ajouter un champ "is_verified" dans le modèle User et le mettre à True
    return {"message": f"L'adresse e-mail de {username} a été vérifiée avec succès !"}




# Route pour obtenir un token d'accès
@router_auth.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Route pour mettre à jour un utilisateur
@router_auth.put("/update_user/{username}")
async def updrouter_authate_user(username: str, update_data: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()

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
    
    return {"message": "Utilisateur mis à jour avec succès", "user": db_user}

# Route pour vérifier la connexion à la base de données
@router.get("/check-db-connection/")
def check_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"message": "Connexion à la base de données réussie !"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de connexion à la base de données : {str(e)}")

oauth2bearer= OAuth2PasswordBearer(tokenUrl='auth/token')
async def get_current_user(token: Annotated[str, Depends(oauth2bearer)]):
    try:
        print(f"Token: {token}")  # Log pour afficher le token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded Payload: {payload}")  # Log pour afficher les données du payload
        
        username: str = payload.get('sub')
        
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user")
        
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user")


##Routes Card
from backend.app.models.Card import Card, CardBase
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency= Annotated[dict,Depends(get_current_user)]
@router_auth.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    return {"User": user}


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
