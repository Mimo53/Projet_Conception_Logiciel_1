from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from backend.app.db.database import Base
from backend.app.models.Card import Card, CardBase

booster_cards = Table(
    'booster_cards', Base.metadata,
    Column('booster_id', Integer, ForeignKey('boosters.id'), primary_key=True),
    Column('card_id', Integer, ForeignKey('cards.id'), primary_key=True)
)


class Booster(Base):
    __tablename__ = 'boosters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    collection_id = Column(Integer, ForeignKey('collections.id'))

    collection = relationship("Collection", back_populates="boosters")
    cards = relationship("Card", secondary="booster_cards", back_populates="boosters")


class BoosterBase(BaseModel):
    name: str
    collection_id: int
    cards: List[CardBase] = []
