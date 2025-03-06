"""
Module définissant le modèle de liaison entre les utilisateurs et les cartes.
"""

from typing import Optional
from pydantic import BaseModel  # Import tiers
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String  # Import tiers
from sqlalchemy.orm import relationship  # Import tiers

from backend.app.db.database import Base

class UserCard(Base):
    """
    Modèle SQLAlchemy représentant la liaison entre un utilisateur et une carte.
    """
    __tablename__ = 'user_cards'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('User.username'))
    card_id = Column(Integer, ForeignKey('cards.id'))
    obtained = Column(Boolean, default=False)

    user = relationship("User", back_populates="user_cards")
    card = relationship("Card")


class UserCardBase(BaseModel):
    """
    Modèle Pydantic pour la liaison entre un utilisateur et une carte.
    """
    user_id: int
    card_id: int
    obtained: Optional[bool] = False
