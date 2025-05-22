from sqlalchemy import Column, Boolean, DateTime
from app.db.config import Base


class DbCreated(Base):
    creation_flag = Column(Boolean, default=False, nullable=False)
    creation_date = Column(DateTime, nullable=False)
