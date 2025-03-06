"""
Module définissant les modèles de données pour les utilisateurs.
"""

from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship

from backend.app.db.database import Base
from backend.app.models.Enums import Role


class User(Base):
    """
    Modèle SQLAlchemy pour les utilisateurs.
    """

    __tablename__ = 'User'

    username = Column(String, primary_key=True, index = True)
    password = Column(String, index=True)
    role = Column(Enum(Role))
    e_mail = Column(String, index=True)

    user_cards = relationship("UserCard", back_populates ="user")


class UserBase(BaseModel):
    """
    Modèle Pydantic pour la création d'un utilisateur.
    """
    username: str
    password: str
    role: Role
    e_mail: EmailStr | None = None


class UserUpdate(BaseModel):
    """
    Modèle Pydantic pour la mise à jour d'un utilisateur.
    """
    new_username: str | None = None
    new_password: str | None = None
    new_email: EmailStr | None = None
