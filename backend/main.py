from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api import (auth_router, booster_router, cards_router,
                             proxy_router)
from backend.app.db import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée")
    yield
    print("Arrêt de l'application")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:8000", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(cards_router)
app.include_router(booster_router)
app.include_router(proxy_router)

@app.get("/api/hello")
async def hello():
    return {"message": "La connexion avec l'API est réussie, amusez-vous bien sur ENSAI TCG !"}
