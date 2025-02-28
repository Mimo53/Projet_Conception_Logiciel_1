from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response
from contextlib import asynccontextmanager
from io import BytesIO
import requests
from fastapi.security import OAuth2PasswordBearer
from backend.app.db.database import Base, engine
import backend.app.api.routes
from backend.app.api.routes import router, router_auth
from backend.app.models import Booster, Card
from backend.app.models.User import User, UserBase

# Définition du cycle de vie de l'application
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code à exécuter au démarrage de l'application
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée")
    yield  # Le serveur démarre ici
    # Code à exécuter à l'arrêt de l'application (facultatif)
    print("Arrêt de l'application")

# Initialisation de l'application FastAPI avec le lifespan
app = FastAPI(lifespan=lifespan)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:8000", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 password bearer (utilisé pour extraire le token d'authentification)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fonction pour vérifier le token (ajuste cette fonction selon ton implémentation)
def verify_token(token: str):
    # Ici tu peux vérifier la validité du token JWT. Pour l'instant, cette fonction est une placeholde
    # Il faut une méthode pour décoder et valider le token JWT avec ta clé secrète
    if token != "ton_token_valide":  # Remplace par ta logique de validation du token JWT
        return False
    return True

@app.get("/image/{file_id}")
async def get_image(file_id: str, token: str = Depends(oauth2_scheme)):
    """
    Cette route permet de récupérer une image depuis Google Drive et de la renvoyer en réponse,
    après avoir validé le token JWT.
    """
    # Vérifier le token JWT
    if not verify_token(token):
        raise HTTPException(status_code=403, detail="Token invalide")

    # L'URL directe de l'image sur Google Drive
    url = f"https://drive.google.com/uc?export=view&id={file_id}"

    try:
        # Effectuer la requête pour récupérer l'image depuis Google Drive
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la requête a réussi (code 200)

        # Retourner l'image sous forme de réponse
        return StreamingResponse(BytesIO(response.content), media_type="image/jpeg")
    except requests.exceptions.RequestException as e:
        # En cas d'erreur, retourner un message d'erreur
        raise HTTPException(status_code=404, detail="Image non trouvée ou erreur de récupération")

@app.get("/api/hello")
async def hello():
    return {"message": "La connexion avec l'API est réussie, amuse-toi bien sur ENSAI TCG !"}

# Inclusion des routes
app.include_router(router)
app.include_router(router_auth)

@app.get("/proxy-image/")
async def proxy_image(url: str):
    try:
        # Utilisation de stream=True pour mieux gérer le flux de données
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Image non trouvée")

        # Détection du Content-Type de l'image
        content_type = response.headers.get("Content-Type", "image/jpeg")
        
        # En-têtes complets pour gérer le CORS et le cache
        headers = {
            "Content-Type": content_type,
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type",
            "Cache-Control": "public, max-age=86400"  # Cache d'un jour
        }

        # Utilisation de Response pour plus de contrôle sur les en-têtes
        return Response(content=response.content, headers=headers, media_type=content_type)
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail="Erreur lors du téléchargement de l'image")