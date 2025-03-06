"""
Module pour la connection de la database pour l'api.

Ce module contient des outils de connections à la base de données postgre
"""

import os

from dotenv import load_dotenv # type: ignore
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les informations de la base de données à partir des variables d'environnement
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

print(f"User: {DATABASE_USER},Password: {DATABASE_PASSWORD}, Host: {DATABASE_HOST}, Port: {DATABASE_PORT}, Name: {DATABASE_NAME}")

# Créer l'URL de connexion pour SQLAlchemy
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Crée une session de base de données et la ferme une fois qu'elle est utilisée.

    Utilisée comme dépendance dans FastAPI pour fournir une session à chaque requête.

    Yields:
        Session: Une session SQLAlchemy liée à la base de données.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
