# app/dependencies.py
from db.config import async_session

# Zależność zarządzająca sesją SQLAlchemy ORM
'''For example, you could use this to create a database session and close it after finishing.

Only the code prior to and including the yield statement is executed before creating a response:'''
async def get_session():
    session = async_session()
    try: #try to catch eg. rollback
        yield session  # Udostępnienie sesji
    finally:
        await session.close()  # Zamknięcie sesji po zakończeniu

