"""
Module des routes du booster pour l'API.

Ce module contient les routes pour ouvrir un booster et ajouter des cartes
à la collection de l'utilisateur, ainsi que pour afficher la collection de cartes
de l'utilisateur.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.services.booster_service import \
    open_booster_and_add as open_booster_service
from backend.app.api.services.booster_service import view_collection
from backend.app.core.security import get_current_user
from backend.app.db.database import get_db

router = APIRouter(prefix='/booster', tags=['booster'])

@router.post("/open_booster_and_add/")
async def open_booster(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Ouvre un booster pour l'utilisateur connecté et ajoute les cartes à sa collection.

    Cette route appelle le service `open_booster_service` pour ouvrir un booster
    et ajouter les cartes à la collection de l'utilisateur. L'utilisateur est
    authentifié via le `get_current_user`, et la session de base de données est
    fournie via `get_db`.

    Args:
        user (dict): L'utilisateur connecté, récupéré par la dépendance `get_current_user`.
        db (Session): La session de base de données, récupérée par la dépendance `get_db`.

    Returns:
        dict: La réponse du service `open_booster_service`, généralement un message
            ou des informations sur les cartes obtenues.
    """
    return await open_booster_service(user, db)

@router.get("/view_collections")
async def collection(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Récupère la collection de cartes de l'utilisateur connecté.

    Cette route récupère toutes les cartes actuellement dans la collection
    de l'utilisateur via le service `view_collection`. L'utilisateur est
    authentifié via `get_current_user`, et la session de base de données est
    fournie via `get_db`.

    Args:
        user (dict): L'utilisateur connecté, récupéré par la dépendance `get_current_user`.
        db (Session): La session de base de données, récupérée par la dépendance `get_db`.

    Returns:
        dict: La collection de cartes de l'utilisateur sous forme d'un dictionnaire.
    """
    return await view_collection(user, db)
