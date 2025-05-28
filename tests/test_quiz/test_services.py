import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.quiz.services import TestService
from app.quiz.models import Question
from app.quiz.schemas import DbQuestion, DbAnswer, AnsweredQuestion
from datetime import datetime

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.quiz.services import TestService
from datetime import datetime

# TEST_SIZE = default_test_size()
# create_test
# random_questions
# get_question
# submit_answer
# validate_question
# validate_answer
# submit_test


@pytest.mark.asyncio
async def test_create_test_with_user(mock_async_session, mock_current_user, default_test_size, mock_random_questions):
    session_mock = mock_async_session
    user = mock_current_user.nick

    # Wywołanie `create_test`
    test_service_instance = await TestService.create_test(user=user, session=session_mock)

    # Assert: Użytkownik poprawnie przypisany do `current_tests`
    assert TestService.current_tests[user] == test_service_instance

    # Sprawdzenie struktury test_service_instance
    assert len(test_service_instance.questions) == default_test_size

    # Sprawdzenie struktury pierwszego pytania
    question = test_service_instance.questions[0]
    assert question.question.id == 1
    assert question.question.question == "Question 1"






#
# @pytest.mark.asyncio
# async def test_random_questions_success(self, mock_async_session, mock_validated_question, mocker):
#     mock_question_validator, mock_answer_validator = mock_validated_question
#
#     # Zamiana MagicMock na mocker.MagicMock
#     mock_result = [
#         mocker.MagicMock(id=i, question=f"Question {i}", answers=[mocker.MagicMock(id=i) for i in range(1, 4)])
#         for i in range(TEST_SIZE)
#     ]
#     mock_async_session.execute.return_value.scalars.return_value.unique.return_value.all.return_value = mock_result
#
#     test_service_instance = await TestService.random_questions(
#         session=mock_async_session,
#         test_size=TEST_SIZE
#     )
#
#     # Assert dla poprawności instancji
#     assert len(test_service_instance.questions) == TEST_SIZE
#     assert isinstance(test_service_instance, TestService)
#
#     # Assert, czy walidatory Pydantic były wywołane
#     assert mock_question_validator.call_count == TEST_SIZE
#     assert mock_answer_validator.call_count == sum([len(q.answers) for q in mock_result])
#
# @pytest.mark.asyncio
# async def test_random_questions_not_enough_questions(self, mock_async_session):
#     # Mock dla pustego wyniku z bazy danych
#     mock_async_session.execute.return_value.scalars.return_value.unique.return_value.all.return_value = []
#
#     with pytest.raises(HTTPException) as exc_info:
#         await TestService.random_questions(
#             session=mock_async_session,
#             test_size=TEST_SIZE
#         )
#
#     assert exc_info.value.status_code == 404
#     assert exc_info.value.detail == "Test questions not found"
#
#
# def test_submit_answer_redirect_on_skip(self, mocker):
#     # Zamiana MagicMock na mocker
#     TestService.current_tests["mockuser"] = TestService(questions=["Q1", "Q2", "Q3", "Q4"])
#     test_instance = TestService.current_tests["mockuser"]
#     test_instance.state = 1  # Obecne pytanie to nr 1
#
#     response = TestService.submit_answer(user="mockuser", id=2, question=None)
#
#     # Assert przekierowania w przypadku próby pominięcia pytania
#     assert response.status_code == 303
#     assert "/frontend/question/1?error=An%20attempt%20to%20skip%20or%20go%20back%20to%20question%20is%20not%20allowed" in response.headers["location"]
#
# @pytest.mark.asyncio
# async def test_submit_test_success(self, mock_async_session, mocker):
#     # Mockujemy instancję TestService przypisaną do użytkownika
#     TestService.current_tests["mockuser"] = TestService(questions=["Q1", "Q2", "Q3", "Q4"])
#
#     test_instance = TestService.current_tests["mockuser"]
#     test_instance.true_ans = 3
#     test_instance.start_time = datetime(2023, 1, 1, 12, 0, 0)
#
#     result = await TestService.submit_test(user="mockuser", session=mock_async_session)
#
#     # Assert dla wyniku
#     assert result["message"] == "test finished, your grade is 75.0 %"
#     mock_async_session.add.assert_called_once()
#     mock_async_session.commit.assert_called_once()
#     mock_async_session.refresh.assert_called_once()
#
#
#
# @pytest.mark.asyncio
# async def test_random_questions_success(mock_async_session, mock_validated_question):
#     mock_question_validator, mock_answer_validator = mock_validated_question
#
#     # Mock dla wyników zapytania SQLAlchemy
#     mock_result = [
#         MagicMock(id=i, question=f"Question {i}", answers=[MagicMock(id=i) for i in range(1, 4)])
#         for i in range(TEST_SIZE)
#     ]
#     mock_async_session.execute.return_value.scalars.return_value.unique.return_value.all.return_value = mock_result
#
#     test_service_instance = await TestService.random_questions(
#         session=mock_async_session,
#         test_size=TEST_SIZE
#     )
#
#     # Assert dla poprawności instancji
#     assert len(test_service_instance.questions) == TEST_SIZE
#     assert isinstance(test_service_instance, TestService)
#
#     # Assert, czy walidatory Pydantic były wywołane
#     assert mock_question_validator.call_count == TEST_SIZE
#     assert mock_answer_validator.call_count == sum([len(q.answers) for q in mock_result])
#
#
# @pytest.mark.asyncio
# async def test_random_questions_not_enough_questions(mock_async_session):
#     mock_async_session.execute.return_value.scalars.return_value.unique.return_value.all.return_value = []
#
#     with pytest.raises(HTTPException) as exc_info:
#         await TestService.random_questions(
#             session=mock_async_session,
#             test_size=TEST_SIZE
#         )
#
#     assert exc_info.value.status_code == 404
#     assert exc_info.value.detail == "Test questions not found"
#
#
# def test_submit_answer_redirect_on_skip():
#     TestService.current_tests["mockuser"] = TestService(questions=["Q1", "Q2", "Q3", "Q4"])
#     test_instance = TestService.current_tests["mockuser"]
#     test_instance.state = 1  # Obecne pytanie to nr 1
#
#     response = TestService.submit_answer(user="mockuser", id=2, question=None)
#
#     # Assert przekierowania w przypadku próby pominięcia pytania
#     assert response.status_code == 303
#     assert "/frontend/question/1?error=An%20attempt%20to%20skip%20or%20go%20back%20to%20question%20is%20not%20allowed" in response.headers["location"]
#
#
# @pytest.mark.asyncio
# async def test_submit_test_success(mock_async_session):
#     TestService.current_tests["mockuser"] = TestService(questions=["Q1", "Q2", "Q3", "Q4"])
#
#     test_instance = TestService.current_tests["mockuser"]
#     test_instance.true_ans = 3
#     test_instance.start_time = datetime(2023, 1, 1, 12, 0, 0)
#
#     result = await TestService.submit_test(user="mockuser", session=mock_async_session)
#
#     # Assert dla wyniku
#     assert result["message"] == "test finished, your grade is 75.0 %"
#     mock_async_session.add.assert_called_once()
#     mock_async_session.commit.assert_called_once()
#     mock_async_session.refresh.assert_called_once()