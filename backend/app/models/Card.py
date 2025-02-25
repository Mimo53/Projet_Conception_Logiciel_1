from pydantic import BaseModel # type: ignore 
from sqlalchemy import Column, Integer, String, Enum # type: ignore

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


