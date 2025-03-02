from io import BytesIO

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response, StreamingResponse
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix='/proxy', tags=['proxy'])

# OAuth2 password bearer pour extraire le token d'authentification
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fonction pour vérifier le token (tu peux ajuster selon ton système JWT)
def verify_token(token: str):
    if token != "ton_token_valide":  # Remplace par ta logique de validation du token JWT
        return False
    return True

@router.get("/proxy-image/")
async def proxy_image(url: str, token: str = Depends(oauth2_scheme)):
    """
    Proxy qui récupère une image externe et la renvoie avec les bons en-têtes CORS.
    Nécessite une authentification via token.
    """
    # Vérifier le token JWT
    if not verify_token(token):
        raise HTTPException(status_code=403, detail="Token invalide")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Image non trouvée")

        # Détection du type de contenu
        content_type = response.headers.get("Content-Type", "image/jpeg")

        headers = {
            "Content-Type": content_type,
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type",
            "Cache-Control": "public, max-age=86400"  # Cache d'un jour
        }

        return Response(content=response.content, headers=headers, media_type=content_type)

    except httpx.RequestError:
        raise HTTPException(status_code=400, detail="Erreur lors du téléchargement de l'image")
