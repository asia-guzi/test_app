from sqlalchemy import Column, Boolean, DateTime  # PrimaryKeyConstraint,
from backend.app.db.config import Base


class DbCreated(Base):
    __tablename__ = "dbcreated"

    creation_flag = Column(Boolean, default=False, nullable=False, primary_key=True)
    creation_date = Column(DateTime, nullable=False, primary_key=True)
