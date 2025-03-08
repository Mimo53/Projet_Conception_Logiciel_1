"""
Module de proxy pour la gestion des images.

Ce module contient une route qui permet de récupérer une image depuis une URL
et de la retourner avec les bons headers HTTP, incluant les informations de cache
et la gestion des CORS.
"""

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

router = APIRouter()

@router.get("/proxy/proxy-image/")
async def proxy_image(url: str):
    """
    Récupère une image depuis l'URL fournie et la retourne avec les bons headers HTTP.

    Cette fonction utilise httpx pour envoyer une requête GET à l'URL de l'image,
    puis retourne l'image avec les en-têtes appropriés pour le CORS et le cache.

    Args:
        url (str): L'URL de l'image à récupérer.

    Returns:
        Response: La réponse contenant l'image avec les headers appropriés.
    """
    try:
        # Utiliser httpx pour envoyer la requête à l'URL de l'image avec suivi des redirections
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail="Erreur de récupération de l'image")

        # Retourner l'image avec les bons headers
        content_type = response.headers.get("Content-Type", "image/jpeg")
        headers = {
            "Content-Type": content_type,
            "Access-Control-Allow-Origin": "*",  # Permet les requêtes cross-origin
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Cache-Control": "public, max-age=86400"  # Cache d'un jour
        }

        return Response(content=response.content,
                        headers=headers,
                        media_type=content_type)

    except httpx.RequestError as exc:
        raise HTTPException(status_code=400,
                            detail="Erreur lors du téléchargement de l'image") from exc
# La ligne vide ici pour pylint
