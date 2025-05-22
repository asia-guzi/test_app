from pymysql.times import TimeDelta
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Boolean, DateTime
from db.config import Base


class DbCreated(Base):
    creation_flag = Column(Boolean, default=False, nullable=False)
    creation_date = Column(DateTime, nullable=False)
