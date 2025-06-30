from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv
import os
from sqlalchemy.orm import DeclarativeBase  # ,


# base for the users
class Base(DeclarativeBase):
    pass


# LOAD ENV VARIABLES .env
load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not configured in .env!")


async_engine = create_async_engine(
    DATABASE_URL
    # , class_ = AsyncSession
    # ,echo=True
)


async_session = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)
