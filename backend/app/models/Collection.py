from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.app.db.database import Base
from backend.app.models.Card import Card, CardBase


class Collection(Base):
    __tablename__ = 'collections'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    cards = relationship("Card", back_populates="collection")


class CollectionBase(BaseModel):
    name: str
    cards: List[CardBase] = []
