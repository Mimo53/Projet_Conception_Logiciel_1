from io import BytesIO

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

router = APIRouter(prefix='/proxy', tags=['proxy'])

@router.get("/proxy-image/")
async def proxy_image(url: str):
    return await proxy_image(url)
