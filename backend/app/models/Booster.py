# backend/app/models/Booster.py
from typing import List
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.app.db.database import Base
from backend.app.models.Card import CardBase
from backend.app.models.Booster_Cards_asso import booster_cards  # Importation de la table

class Booster(Base):
    __tablename__ = 'boosters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    collection_id = Column(Integer, ForeignKey('collections.id'))

    collection = relationship("Collection", back_populates="boosters")
    cards = relationship("Card", secondary=booster_cards, back_populates="boosters")


class BoosterBase(BaseModel):
    name: str
    collection_id: int
    cards: List[CardBase] = []
