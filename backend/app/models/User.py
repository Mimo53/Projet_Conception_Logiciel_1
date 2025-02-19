from ..models.Enums import Role
from ..db.database import Base, get_db
from sqlalchemy import Column, String
from pydantic import BaseModel

class User:
    def __init__(self, username: str, password: str, role: Role):
        self.username = username
        self.password = password  # À hasher
        self.role = role

class User(Base):
    __tablename__='User'

    username= Column(String, primary_key=True,index=True)
    password = Column(String,index=True)
    role = Column(String,index=True)
    e_mail= Column(String,index=True)

class UserBase(BaseModel):
    username: str
    password: str
    role: str
    e_mail: str
