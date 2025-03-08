"""
Module contenant les classes nécessaires à l'utilisation
des utilisateurs dans le projets
"""

from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship

from backend.app.db.database import Base
from backend.app.models.enums import Role


class User(Base):
    """
    Classe représentant un utilisateur dans la base de données.
    """
    __tablename__ = 'User'

    username = Column(String, primary_key=True, index = True)
    password = Column(String, index=True)
    role = Column(Enum(Role))
    e_mail = Column(String, index=True)

    user_cards = relationship("UserCard", back_populates ="user")


class UserBase(BaseModel):
    """
    Schéma de base pour la création d'un utilisateur.
    """
    username: str
    password: str
    role: Role
    e_mail: EmailStr | None = None


class UserUpdate(BaseModel):
    """
    Schéma pour mettre à jour un utilisateur existant.
    """
    new_username: str | None = None
    new_password: str | None = None
    new_email: EmailStr | None = None
