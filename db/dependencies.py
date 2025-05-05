# app/dependencies.py
from db.config import async_session

# Zależność zarządzająca sesją SQLAlchemy ORM
async def get_session():
    session = async_session()
    try:
        yield session  # Udostępnienie sesji
    finally:
        await session.close()  # Zamknięcie sesji po zakończeniu

