# backend/app/db/models.py

from sqlalchemy import Column, Integer, String, Enum
from backend.app.db.database import Base  # Importation de Base depuis database.py

# Importer Rarity ici
from backend.app.models.enums import Rarity

class Card(Base):
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

