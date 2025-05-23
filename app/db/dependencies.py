# app/dependencies.py
from .config import async_session
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncSession:
    """
    Returns database session

    :return: AsyncSession - An instance containing the selected questions.
    """
    # session = async_session()
    # try: #try to catch eg. rollback
    #     yield session  # Udostępnienie sesji
    # finally:
    #     await session.close()  # Zamknięcie sesji po zakończeniu
    async with async_session() as session:
        yield session
