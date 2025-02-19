from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, String
from backend.app.db.database import get_db
from backend.app.models.User import User,UserBase
router = APIRouter()


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
