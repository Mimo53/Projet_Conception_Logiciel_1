from fastapi import APIRouter, HTTPException
import httpx
from fastapi.responses import Response

router = APIRouter()

@router.get("/proxy/proxy-image/")
async def proxy_image(url: str):
    try:
        # Utiliser httpx pour envoyer la requête à l'URL de l'image avec suivi des redirections
        async with httpx.AsyncClient(follow_redirects=True) as client:  # Activer le suivi des redirections
            response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Erreur de récupération de l'image")

        # Retourner l'image avec les bons headers
        content_type = response.headers.get("Content-Type", "image/jpeg")
        headers = {
            "Content-Type": content_type,
            "Access-Control-Allow-Origin": "*",  # Permet les requêtes cross-origin
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Cache-Control": "public, max-age=86400"  # Cache d'un jour
        }

        return Response(content=response.content, headers=headers, media_type=content_type)

    except httpx.RequestError:
        raise HTTPException(status_code=400, detail="Erreur lors du téléchargement de l'image")
