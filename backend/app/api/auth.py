from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt

from backend.app.db.database import get_db
from backend.app.models.User import User

# Clé secrète pour signer les tokens JWT (change-la en production !)
SECRET_KEY = "ma_super_cle_secrete"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Hashing des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 pour gérer les tokens JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

def hash_password(password: str) -> str:
    """ Hash le mot de passe en utilisant bcrypt """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Vérifie si un mot de passe correspond au hash """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """ Crée un token JWT pour un utilisateur """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """ Récupère l'utilisateur connecté à partir du token JWT """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalide")
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="Utilisateur non trouvé")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide")

@router.post("/register")
async def register_user(user: User, db: Session = Depends(get_db)):
    """ Permet à un utilisateur de s'inscrire """
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")

    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, password=hashed_password, role=user.role, e_mail=user.e_mail)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Utilisateur créé avec succès"}

@router.post("/token")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """ Authentifie un utilisateur et génère un token JWT """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

    token = create_access_token(data={"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}
