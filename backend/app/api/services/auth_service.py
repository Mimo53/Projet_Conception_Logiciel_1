"""
Module contenant les services d'authentification.

Ce module inclut les fonctions pour gérer l'authentification des utilisateurs,
le hashage des mots de passe, la génération de jetons d'accès et la validation
des utilisateurs via des tokens JWT.
"""

import os
from dotenv import load_dotenv
from datetime import timedelta,datetime
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.models.User import User,UserBase

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Accéder aux variables d'environnement
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    """
    Vérifie si le mot de passe en clair correspond au mot de passe haché.

    Args:
        plain_password (str): Le mot de passe en clair.
        hashed_password (str): Le mot de passe haché.

    Returns:
        bool: Retourne True si les mots de passe correspondent, sinon False.
    """
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str):
    """
    Hache le mot de passe fourni en utilisant l'algorithme bcrypt.

    Args:
        password (str): Le mot de passe en clair à hacher.

    Returns:
        str: Le mot de passe haché.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Crée un jeton d'accès JWT signé à partir des données spécifiées.

    Args:
        data (dict): Un dictionnaire contenant les informations à inclure dans le jeton.
        expires_delta (timedelta | None, optional): 
        La durée d'expiration du jeton. Si None, la valeur par défaut est 15 minutes.

    Returns:
        str: Le jeton d'accès JWT encodé.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str, db: Session):
    """
    Authentifie un utilisateur en vérifiant ses informations d'identification.

    La fonction recherche un utilisateur dans la base de données en fonction du nom d'utilisateur
    et vérifie si le mot de passe fourni correspond au mot de passe haché stocké.

    Args:
        username (str): Le nom d'utilisateur à authentifier.
        password (str): Le mot de passe en clair à vérifier.
        db (Session): La session de base de données pour interagir avec la table des utilisateurs.

    Returns:
        User | None: L'utilisateur trouvé si les informations sont valides, sinon None.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Récupère l'utilisateur actuellement authentifié à partir du jeton JWT.

    Cette fonction décode le jeton JWT, extrait le nom d'utilisateur, et recherche l'utilisateur
    correspondant dans la base de données. Si l'utilisateur est trouvé, il renvoie un dictionnaire
    contenant le nom d'utilisateur, l'email et le rôle de l'utilisateur. Si le jeton est invalide ou
    l'utilisateur n'est pas trouvé, une exception HTTP est levée.

    Args:
        token (str, optional): Le jeton d'accès JWT fourni par l'utilisateur,
        par défaut obtenu via OAuth2PasswordBearer.
        db (Session, optional): La session de base de données pour interagir avec la table des utilisateurs.

    Raises:
        HTTPException: 
            - 401 si le jeton est invalide ou si l'utilisateur ne peut pas être validé.
            - 404 si l'utilisateur n'est pas trouvé dans la base de données.

    Returns:
        dict: Un dictionnaire contenant les informations de l'utilisateur 
        (username, email, role) si authentifié avec succès.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate user")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"username": username, "email": user.e_mail, "role": user.role}
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Could not validate user") from exc

