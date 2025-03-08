# backend/app/models/card_model.py

from pydantic import BaseModel  # type: ignore
from sqlalchemy import Column, Integer, String, Enum  # type: ignore
from backend.app.models.enums import Rarity  # Reste inchangé
from backend.app.db.database import Base  # Utilisation directe de Base

class Card(Base):  # Utilisation de Base directement
    """
    Représente une carte dans la base de données.
    """
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image_url = Column(String)
    rarity = Column(Enum(Rarity))

    def __repr__(self):
        return f"<Card(id={self.id}, name={self.name}, rarity={self.rarity})>"

class CardBase(BaseModel):
    """
    Modèle Pydantic pour la validation des données d'une carte.
    """
    name: str
    image_url: str
    rarity: Rarity
    # noqa: R0903
