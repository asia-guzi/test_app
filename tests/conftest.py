# file for pytest to find fixtures
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock
from app.users.models import User
import pytest




@pytest.fixture
def mock_async_session(mocker):
    """
     mock async session
     """
    return mocker.MagicMock()

# Deliver user
@pytest.fixture
def mock_current_user():
    user = User(
        nick='test_nick',
        save_password='test_pass',
        name='test_name',
        surname='test_surname',
        email='test_em@a.il',
        role='student'

    )
    return user

