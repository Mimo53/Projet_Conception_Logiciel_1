from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from backend.app.db.database import Base
from backend.app.models.Enums import Role


class User(Base):
    __tablename__ = 'User'

    username = Column(String, primary_key=True, index = True)
    password = Column(String, index=True)
    role = Column(String, index=True)
    e_mail = Column(String, index=True)

    user_cards = relationship("UserCard", back_populates =" user")
    

class UserBase(BaseModel):
    username: str 
    password: str 
    role: Role 
    e_mail: EmailStr | None = None 


class UserUpdate(BaseModel):
    new_username: str | None = None
    new_password: str | None = None
    new_email: EmailStr | None = None