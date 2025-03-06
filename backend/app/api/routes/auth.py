from datetime import timedelta

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.api.services.auth_service import (authenticate_user,
                                                   create_access_token,
                                                   get_current_user,
                                                   hash_password)
from backend.app.api.services.email_service import send_verification_email
from backend.app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.app.db.database import get_db
from backend.app.models.User import User, UserBase, UserUpdate


# Définir la classe Token
class Token(BaseModel):
    access_token: str
    token_type: str

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post("/register", status_code=201)
async def register_user(user: UserBase, db: Session = Depends(get_db), background_tasks: BackgroundTasks = BackgroundTasks()):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="L'utilisateur existe déjà")

    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        password=hashed_password,
        role=user.role,
        e_mail=user.e_mail,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    if db_user.e_mail:
        background_tasks.add_task(send_verification_email, db_user.e_mail, db_user.username)

    return {"message": "Utilisateur créé avec succès, vérifiez votre e-mail", "user": db_user}

@router.get("/verify-email/{username}")
async def verify_email(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"message": f"L'adresse e-mail de {username} a été vérifiée avec succès !"}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": str(user.role)},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/update_user/{username}")
async def update_user(username: str, update_data: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    if update_data.new_username:
        existing_user = db.query(User).filter(User.username == update_data.new_username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Ce nom d'utilisateur est déjà pris")
        db_user.username = update_data.new_username

    if update_data.new_password:
        db_user.password = hash_password(update_data.new_password)

    db.commit()
    db.refresh(db_user)

    return {"message": "Utilisateur mis à jour avec succès", "user": db_user}
