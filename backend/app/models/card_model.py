"""
Module définissant les classes de carte pour la base de données et le modèle Pydantic.

Ce module contient la classe `Card`, qui est une représentation d'une carte dans la base de données,
ainsi que `CardBase`, un modèle Pydantic pour la validation des données de carte.
"""

from pydantic import BaseModel # type: ignore
from sqlalchemy import Column, Integer, String, Enum # type: ignore

from backend.app.db.database import Base
from backend.app.models.enums import Rarity

class Card(Base):
    """
    Représente une carte dans la base de données.

    Attributs :
        id (int) : L'identifiant de la carte.
        name (str) : Le nom de la carte.
        image_url (str) : L'URL de l'image de la carte.
        rarity (Rarity) : La rareté de la carte.
    """
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image_url = Column(String)
    rarity = Column(Enum(Rarity))

    def __repr__(self):
        """
        Représente la carte sous forme de chaîne de caractères.

        Cela permet d'afficher plus clairement les informations d'une carte
        lorsque celle-ci est affichée dans le terminal ou dans les logs.
        """
        return f"<Card(id={self.id}, name={self.name}, rarity={self.rarity})>"


class CardBase(BaseModel):
    """
    Modèle Pydantic pour la validation des données d'une carte.

    Attributs :
        name (str) : Le nom de la carte.
        image_url (str) : L'URL de l'image de la carte.
        rarity (Rarity) : La rareté de la carte.
    """
    name: str
    image_url: str
    rarity: Rarity
    # noqa: R0903
