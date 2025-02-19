from pydantic import BaseModel
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.app.db.database import Base
from backend.app.models.Enums import Rarity


class Card:
    def __init__(self, name: str, image_url: str, rarity: Rarity):
        self.name = name
        self.image_url = image_url
        self.rarity = rarity


class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image_url = Column(String)
    rarity = Column(Enum(Rarity))
    collection_id = Column(Integer, ForeignKey('collections.id'))

    collection = relationship("Collection", back_populates="cards")


class CardBase(BaseModel):
    name: str
    image_url: str
    rarity: Rarity

