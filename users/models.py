
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from db.config import Base
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr




from sqlalchemy import Column, Integer, , ForeignKey, Boolean, PrimaryKeyConstraint
from db.config import Base #, async_engine



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nick =  Column(String)
   - password = Column(String)
    name = Column(String)
    surname = Column(String)
    role = Column(String) #student / teacher
    email = EmailStr
    users = relationship("User", back_populates="tests")

#access do start test i do wynik test przydzielonego przez teacher



