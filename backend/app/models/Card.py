from pydantic import BaseModel
from sqlalchemy import (Boolean, Column, Enum, ForeignKey, Integer, String,
                        Table)
from sqlalchemy.orm import relationship

from backend.app.db.database import Base
from backend.app.models.Enums import Rarity

# Table d'association pour la relation entre les cartes et collections
collection_cards = Table(
    'collection_cards', Base.metadata,
    Column('card_id', Integer, ForeignKey('cards.id'), primary_key=True),
    Column('collection_id', Integer, ForeignKey('collections.id'), primary_key=True)
)


class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image_url = Column(String)
    rarity = Column(Enum(Rarity))
    is_approved = Column(Boolean, default=False)

    collections = relationship("Collection", secondary=collection_cards, back_populates="cards")
    boosters = relationship("Booster", secondary="booster_cards", back_populates="cards")


class CardBase(BaseModel):
    name: str
    image_url: str
    rarity: Rarity
