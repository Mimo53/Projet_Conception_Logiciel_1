from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.app.db.database import Base
from backend.app.models.Card import Card, CardBase


class Booster(Base):
    __tablename__ = 'boosters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    cards = relationship("Card", back_populates="booster")


class BoosterBase(BaseModel):
    name: str
    cards: List[CardBase] = []

