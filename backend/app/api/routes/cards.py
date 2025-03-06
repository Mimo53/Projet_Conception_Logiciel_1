from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.api.services.card_service import add_card, get_cards
from backend.app.core.security import get_current_user
from backend.app.db.database import get_db
from backend.app.models.Card import Card, CardBase
from backend.app.models.Enums import Role

router = APIRouter(prefix='/cards', tags=['cards'])

@router.get("/")
async def read_cards(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return await get_cards(skip, limit, db)

@router.post("/")
async def create_card(card_data: CardBase, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await add_card(card_data, db, current_user)
