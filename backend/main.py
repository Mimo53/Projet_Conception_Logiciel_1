from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import backend.app.api.routes
from backend.app.api.routes import router, router_auth
from backend.app.db.database import Base, engine
from backend.app.models import (  # Importe tous les modèles nécessaires
    Booster, Card)

from backend.app.models.User import User, UserBase

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/hello")
async def hello():
    return {"message": "La connexion avec l'API est réussi, amuse toi bien sur ENSAI TCG !"}

app.include_router(router)
app.include_router(router_auth)
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
