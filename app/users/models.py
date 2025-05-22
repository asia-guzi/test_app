
from sqlalchemy import String, Enum
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, Boolean
from app.db.config import Base #, async_engine



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nick =  Column(String(50), nullable=False, unique=True)
    save_password = Column(String(64), nullable=False)
    name = Column(String(50))
    #ddoac nullable false
    surname = Column(String(50))
    email = Column(String(50))
    role = Column(Enum('student', 'teacher', name='role_enum')) # 2 possible values
    disabled = Column(Boolean, default=False)
    tests = relationship("TestResult", back_populates="user")


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

