"""
Module principal de l'API ENSAI TCG.

Ce module initialise l'application FastAPI, configure CORS et inclut les routeurs.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api import auth_router, booster_router, cards_router, proxy_router
from backend.app.db import Base, engine


@asynccontextmanager
async def lifespan(app=FastAPI):
    """
    Gère le cycle de vie de l'application FastAPI.
    Initialise la base de données au démarrage et affiche un message lors de l'arrêt.
    """
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée")
    yield
    print("Arrêt de l'application")


app = FastAPI(lifespan=lifespan)

# Configuration du middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:8000",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:8000/proxy/proxy-image/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routeurs
app.include_router(auth_router)
app.include_router(cards_router)
app.include_router(booster_router)
app.include_router(proxy_router)

# Affichage des routes disponibles
for route in app.routes:
    print(route.path)


@app.get("/api/hello")
async def hello():
    """
    Vérifie la connexion avec l'API.
    Retourne un message de bienvenue.
    """
    return {"message": "La connexion avec l'API est réussie, amusez-vous bien sur ENSAI TCG !"}

# Ajout d'une seule ligne vide à la fin du fichier
