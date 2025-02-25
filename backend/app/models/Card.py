# backend/app/models/Card.py
from pydantic import BaseModel
from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from backend.app.db.database import Base
from backend.app.models.Enums import Rarity

class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image_url = Column(String)
    rarity = Column(Enum(Rarity))


class CardBase(BaseModel):
    name: str
    image_url: str
    rarity: Rarity
