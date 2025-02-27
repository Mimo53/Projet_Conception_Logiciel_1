import os
import requests
import httpx
from datetime import datetime, timedelta
from email.mime.image import \
    MIMEImage  
from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import Annotated, List

from fastapi import (APIRouter, BackgroundTasks, Depends, File, HTTPException,
                    UploadFile, status)
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_mail import FastMail, MessageSchema
from jose import ExpiredSignatureError, JWTError, jwt # type: ignore
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import Session
from starlette import status

from backend.app.db.database import get_db
from backend.app.models.mail import conf
from backend.app.models.User import User, UserBase, UserUpdate
from backend.app.models.UserCard import UserCard, UserCardBase

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
router_proxy = APIRouter()

fm = FastMail(conf)

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
    
    # Ajoute le rôle de l'utilisateur dans le token
    to_encode.update({"role": data.get("role")})
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
    # Ajoute le rôle de l'utilisateur dans le token
    access_token = create_access_token(
        data={
            "sub": user.username,
            "role": str(user.role)  # Ajout du rôle ici
        }, 
        expires_delta=access_token_expires
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
async def get_current_user(token: str = Depends(oauth2bearer), db: Session = Depends(get_db)):
    try:
        print(f"Token: {token}")  # Log pour afficher le token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded Payload: {payload}")  # Log pour afficher les données du payload

        username: str = payload.get("sub")
        role: str = payload.get("role")  # Récupération du rôle depuis le token

        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user")

        # Récupérer l'utilisateur à partir de la base de données en utilisant le nom d'utilisateur
        user = db.query(User).filter(User.username == username).first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Retourne un dictionnaire avec le nom d'utilisateur et l'email (utiliser e_mail)
        return {"username": username, "email": user.e_mail, "role": role}  # Utilisation correcte de e_mail

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user")

async def send_email_with_attachment(file_content: bytes):
    try:
        # Créer un fichier temporaire en mémoire avec le contenu du fichier
        with NamedTemporaryFile(delete=False, mode="wb") as tmp_file:
            tmp_file.write(file_content)
            tmp_file_path = tmp_file.name
        
        # Créer un objet message avec l'email du destinataire
        message = MessageSchema(
            subject="Voici l'image que vous avez envoyée",
            recipients=[conf.MAIL_USERNAME],  # L'adresse email de destination
            body="Voici l'image que vous avez envoyée en pièce jointe.",
            subtype="html",
            attachments=[{
                "file": tmp_file_path,  # Le fichier temporaire
                "filename": "image.jpg",  # Nom du fichier
                "type": "image/jpeg"  # Type MIME de l'image
            }]
        )

        # Envoi du message
        await fm.send_message(message)
        print("Email envoyé à l'équipe d'ENSAI TCG avec l'image.")
        
        # Supprimer le fichier temporaire après l'envoi de l'email
        os.remove(tmp_file_path)
        
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")

# Route pour recevoir l'image et l'envoyer par email
@router.post("/upload-and-send/")
async def upload_and_send(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Recevoir un fichier image et l'envoyer par email."""
    
    # Vérification du type de fichier (image)
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Format de fichier non supporté")

    # Lire immédiatement le contenu du fichier (en mémoire)
    file_content = await file.read()

    # Ajouter l'envoi de l'email en tâche de fond
    background_tasks.add_task(send_email_with_attachment, file_content=file_content)

    return {"message": "L'image a été reçue et sera envoyée par email."}

##Routes Card
from backend.app.models.Card import Card, CardBase

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency= Annotated[dict,Depends(get_current_user)]

@router_auth.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    # Affiche le nom d'utilisateur et l'email
    return {"User": user}

@router.get("/cards/")
async def read_cards(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cards = db.query(Card).offset(skip).limit(limit).all()
    return cards




##Routes Booster

from backend.app.models.Booster import BoosterBuilder
#ouvrir booster
from backend.app.models.UserCard import UserCard
from backend.app.services.BoosterService import BoosterService


@router.post("/open_booster_and_add/")
async def open_booster_and_add(user: user_dependency,db: Session = Depends(get_db)):
    user_id = user["username"]
    builder = BoosterBuilder(db)
    cards = builder.with_random_cards().build()

    user_cards = []
    for card in cards:
        # Ajout de la carte à l'utilisateur
        user_card = UserCard(user_id=user_id, card_id=card.id, obtained=True)
        db.add(user_card)

        # Conversion de l'objet SQLAlchemy en dict pour l'affichage
        user_cards.append({
            "id": card.id,
            "name": card.name,
            "image_url": card.image_url,  
            "rarity": card.rarity.name  
        })

    db.commit()

    return {"message": "Booster ouvert et cartes ajoutées à l'utilisateur.", "cards": user_cards}

@router.get("/view_collections")
async def view_collection(user: user_dependency,db: Session = Depends(get_db)):
    user_id = user["username"]
# Récupérer toutes les cartes associées à l'utilisateur    
    user_cards = (
        db.query(UserCard)
        .join(Card, UserCard.card_id == Card.id)  # Jointure pour récupérer les infos des cartes
        .filter(UserCard.user_id == user_id, UserCard.obtained == True)  # Filtrer par user_id et cartes obtenues
        .all()
    )

    if not user_cards:
        raise HTTPException(status_code=404, detail="Aucune carte trouvée pour cet utilisateur.")

    # Formater la réponse en JSON avec les infos des cartes
    collection = [
        {
            "card_name": user_card.card.name,
            "image_url": user_card.card.image_url,
            "rarity": user_card.card.rarity.name  # Assure-toi que `rarity` est bien une Enum
        }
        for user_card in user_cards
    ]

    return {"user_id": user_id, "collection": collection}

from backend.app.models.Enums import Role


@router.post("/cartes_ajout")
async def card_ajout(user: user_dependency, card_data: CardBase, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur est Admin
    if user["role"] != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Accès interdit : Vous devez être administrateur pour ajouter des cartes")

    # Création de la carte
    new_card = Card(
        name=card_data.name,
        image_url=card_data.image_url,
        rarity=card_data.rarity
    )

    db.add(new_card)
    db.commit()
    db.refresh(new_card)

    return {"message": "Carte ajoutée avec succès", "card": new_card}

@router.get("/auth/user_id")
async def get_user_id(current_user: dict = Depends(get_current_user)):
    return {"user_id": current_user["username"]}

@router_proxy.get("/proxy-image/")
async def proxy_image(url: str):
    print(f"URL reçue par le backend : {url}")  # Affiche l'URL dans les logs du serveur
    
    if not url.startswith("https://drive.google.com/uc?export=view&id="):
        print("URL incorrecte")
        raise HTTPException(status_code=400, detail="URL non valide")
   
    # Autres traitements pour récupérer l'image
    try:
        # Effectuer une requête GET sur l'URL de l'image avec httpx
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url)

        # Afficher les en-têtes pour déboguer
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        # Vérifier que la requête a réussi
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Image not found")

        # Déterminer le type MIME du fichier
        content_type = response.headers.get("Content-Type", "application/octet-stream")
        
        # Retourner l'image en tant que StreamingResponse
        image_stream = BytesIO(response.content)
        return StreamingResponse(image_stream, media_type=content_type)
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du téléchargement de l'image: {str(e)}")
