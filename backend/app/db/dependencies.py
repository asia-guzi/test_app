from .config import async_session
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncSession:
    """
    Returns database session

    :return: AsyncSession - An instance containing the selected questions.
    """

    async with async_session() as session:
        yield session
