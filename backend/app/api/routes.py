from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, File, UploadFile
from passlib.context import CryptContext
from sqlalchemy import Column, String
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import timedelta, datetime
from jose import jwt, JWTError,ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from backend.app.db.database import get_db
from backend.app.models.User import User, UserBase, UserUpdate
from backend.app.models.UserCard import UserCard, UserCardBase
from starlette import status
from fastapi_mail import FastMail, MessageSchema
from backend.app.models.mail import conf
from io import BytesIO
from email.mime.image import MIMEImage  # Importer MIMEImage pour manipuler les images
import os 
from tempfile import NamedTemporaryFile
from fastapi.responses import HTMLResponse,JSONResponse

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
async def get_current_user(token: str = Depends(oauth2bearer), db: Session = Depends(get_db)):
    try:
        print(f"Token: {token}")  # Log pour afficher le token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded Payload: {payload}")  # Log pour afficher les données du payload

        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user")

        # Récupérer l'utilisateur à partir de la base de données en utilisant le nom d'utilisateur
        user = db.query(User).filter(User.username == username).first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Retourne un dictionnaire avec le nom d'utilisateur et l'email (utiliser e_mail)
        return {"username": username, "email": user.e_mail}  # Utilisation correcte de e_mail

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




##Routes Booster

from backend.app.services.BoosterService import BoosterService
from backend.app.models.Booster import BoosterBuilder

#ouvrir booster
from backend.app.models.UserCard import UserCard

@router.post("/open_booster_and_add/")
async def open_booster_and_add(user_id: str, db: Session = Depends(get_db)):
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
            "image_url": card.image_url,  # ✅ On récupère l'URL
            "rarity": card.rarity.name  # ✅ Conversion en string pour JSON
        })

    db.commit()

    return {"message": "Booster ouvert et cartes ajoutées à l'utilisateur.", "cards": user_cards}


@router.get("/cards/{card_id}")
async def get_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carte non trouvée")

    return {
        "id": card.id,
        "name": card.name,
        "image_url": card.image_url,
        "rarity": card.rarity.name
    }

@router.get("/view_card/{card_id}", response_class=HTMLResponse)
async def get_cards(db: Session = Depends(get_db)):
    cards = db.query(Card).all()
    return [
        {
            "name": card.name, 
            "image_url": card.image_url, 
            "rarity": card.rarity.name  # ✅ Convertir Rarity en string
        } 
        for card in cards
    ]