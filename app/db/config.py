# app/config.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv
import os
from sqlalchemy.orm import DeclarativeBase #,


#base for the users
class Base(DeclarativeBase):
    pass


# LOAD ENV VARIABLES .env
load_dotenv()


# get the adres of db, universal url, in order to allow
# changes to be made only in .env in case parameters change
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not configured in .env!")


# create engine - async (library mostly writen in C)- due to assumption that
# 'countless' pupils can try to generate and pass tests at one time
async_engine = create_async_engine(
    DATABASE_URL
    # , class_ = AsyncSession
    # ,echo=True
)


# session to get data from db
async_session = async_sessionmaker(
    bind=async_engine
    , class_=AsyncSession
    , expire_on_commit=False
    # need it not to download info about questions 2 times -> for geting and for validfation
)

