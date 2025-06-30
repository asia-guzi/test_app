from app.users.models import User
import pytest


@pytest.fixture
def mock_current_user():
    """
    deliver User instance
    """
    user = User(
        id=1,
        nick="test_nick",
        save_password="test_pass",
        name="test_name",
        surname="test_surname",
        email="test_em@a.il",
        role="student",
    )
    return user
