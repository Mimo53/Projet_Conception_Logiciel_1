from io import BytesIO

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, StreamingResponse

router = APIRouter(prefix='/proxy', tags=['proxy'])

@router.get("/proxy-image/")
async def proxy_image(url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Image non trouvée")

        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type",
            "Content-Type": response.headers.get("Content-Type", "image/jpeg"),
        }

        return Response(content=response.content, headers=headers, media_type="image/jpeg")
    
    except httpx.RequestError:
        raise HTTPException(status_code=400, detail="Erreur lors du téléchargement de l'image")
