
from sqlalchemy import Column, String, Integer, CheckConstraint, Enum
from sqlalchemy.orm import relationship
from db.config import Base
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr




from sqlalchemy import Column, Integer, ForeignKey, Boolean, PrimaryKeyConstraint
from db.config import Base #, async_engine



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nick =  Column(String)
    password = Column(String)
    name = Column(String)
    surname = Column(String)
    role = Column(String) #student / teacher
    =email = EmailStr
    role = Column(Enum('student', 'teacher', name='role_enum')) # 2 possible values
    disabled : Boolean = False
    users = relationship("User", back_populates="tests")


    """
    check constraint jak w sql:
    __table_args__ = (
        CheckConstraint("status IN ('active', 'inactive')", name='chk_status'),
    )
    
    check constraint jak w sql,k ale mozna 2 kolumny uzyc.
    __table_args__ = (
        CheckConstraint("end_date > start_date", name='chk_date_order'),
    )
    
    price = Column(Integer, CheckConstraint('price > 0', name='chk_positive_price'), nullable=False)
    status = Column(Enum('active', 'inactive', name='status_enum'), nullable=False)


    #access do start test i do wynik test przydzielonego przez teacher
    
    """

