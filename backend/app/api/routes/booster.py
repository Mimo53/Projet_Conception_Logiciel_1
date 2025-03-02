from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.api.services.booster_service import \
    open_booster_and_add as open_booster_service
from backend.app.api.services.booster_service import view_collection
from backend.app.core.security import get_current_user
from backend.app.db.database import get_db

router = APIRouter(prefix='/booster', tags=['booster'])

@router.post("/open_booster_and_add/")
async def open_booster(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return await open_booster_service(user, db)  # 🔥 On appelle bien le service ici !

@router.get("/view_collection")
async def collection(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return await view_collection(user, db)
