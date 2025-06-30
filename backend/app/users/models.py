from sqlalchemy import String, Enum
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, Boolean
from app.db.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nick = Column(String(50), nullable=False, unique=True)
    save_password = Column(String(64), nullable=False)
    name = Column(String(50))
    surname = Column(String(50))
    email = Column(String(50))
    role = Column(Enum("student", "teacher", name="role_enum"))  # 2 possible values
    disabled = Column(Boolean, default=False)
    tests = relationship("TestResult", back_populates="user")
