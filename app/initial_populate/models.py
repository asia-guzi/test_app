from sqlalchemy import Column, Boolean, DateTime  #PrimaryKeyConstraint,
from app.db.config import Base


class DbCreated(Base):
    __tablename__ = "dbcreated"

    creation_flag = Column(Boolean, default=False, nullable=False, primary_key=True)
    creation_date = Column(DateTime, nullable=False, primary_key=True)

    # __table_args__ = (
    #     PrimaryKeyConstraint('creation_flag', 'creation_date', name='flagPK')
    # ) # second option - instead of primary


