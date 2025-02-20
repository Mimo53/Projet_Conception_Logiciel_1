from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.app.db.database import Base


class UserCard(Base):
    __tablename__ = 'user_cards'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('User.username'))
    card_id = Column(Integer, ForeignKey('cards.id'))
    obtained = Column(Boolean, default=False)

    user = relationship("User", back_populates="user_cards")
    card = relationship("Card")


class UserCardBase(BaseModel):
    user_id: int
    card_id: int
    obtained: Optional[bool] = False

