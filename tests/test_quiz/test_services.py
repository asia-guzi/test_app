import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from app.quiz.services import TestService
from app.quiz.models import Question
from app.quiz.schemas import DbQuestion, DbAnswer, AnsweredQuestion, GetQuestion
from datetime import datetime

import pytest
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import SQLAlchemyError
from app.quiz.services import TestService
from datetime import datetime
from tests.test_quiz.helpers import get_AnsweredQuestion_schema, mock_user_responses_collection


# TEST_SIZE = default_test_size()
#-- create_test
# random_questions
# get_question
# submit_answer
# validate_question
# validate_answer
# submit_test

@pytest.mark.asyncio
async def test_get_question_in_right_order_success(data_for_tests, mock_test_service_instance_bounded, mock_current_user, default_test_size):
    user = mock_current_user.nick
    test_instance = TestService.current_tests[user]
    test_raw_data = data_for_tests

    size = default_test_size
    for id in range(size):
        result = await TestService.get_question(user, id+1)
        compare = test_raw_data[id]

        test_instance.state += 1 # mock a part from tesrservice.submit_answer
        assert isinstance(result, GetQuestion)
        assert result.question == compare["question"]

@pytest.mark.asyncio
async def test_get_question_fail(data_for_tests, mock_test_service_instance_bounded, mock_current_user, default_test_size):
    def compare_redirect_responses(response1: RedirectResponse, response2: RedirectResponse) -> bool:
        return (
                response1.status_code == response2.status_code and
                response1.headers.get("location") == response2.headers.get("location")
        )

    user = mock_current_user.nick
    test_instance = TestService.current_tests[user]
    id = 2
    test_instance.state = id # mock a part from tesrservice.submit_answer

    error_message = "An attempt to skip or go back to question is not allowed"
    compare =  RedirectResponse(url=f"/question/{id}?error={error_message}")

    cases = {
        'out_of_range_id' : default_test_size + 2
        , 'negative_id' : -2
        , 'skip_question' : id + 1
        , 'redo_question' : id - 1
    }

    for id in cases.values():
        result = await TestService.get_question(user, id)
        assert isinstance(compare, RedirectResponse)
        assert True == compare_redirect_responses(result, compare)



@pytest.mark.asyncio
async def test_create_test_with_user(mock_async_session, mock_current_user, default_test_size, mock_random_questions):

    session_mock = mock_async_session
    user = mock_current_user.nick

    # call create_test
    test_service_instance = await TestService.create_test(user=user, session=session_mock)

    #assert if function returns right class instance
    assert isinstance(test_service_instance, TestService)

    # assert if test not properly bound with user
    assert TestService.current_tests[user] == test_service_instance



@pytest.mark.asyncio
async def test_submit_answer_success():
    pass



def test_validate_question_success(mock_user_true_responses,
                                    mock_test_service_instance_bounded, mock_current_user, data_for_tests, mock_validate_answer):

    test = mock_test_service_instance_bounded
    for response in mock_user_true_responses:
        success_result = test.validate_question(response)
        test.state += 1
        assert success_result is None


def test_validate_question_fail(mock_user_true_false,
                                    mock_test_service_instance_bounded, mock_current_user, data_for_tests, mock_validate_answer):

    test = mock_test_service_instance_bounded
    for response in mock_user_true_false:
        with pytest.raises(HTTPException) as result:
            test.validate_question(response)
        test.state += 1
        assert isinstance(result.value, HTTPException)
        assert result.value.status_code == status.HTTP_400_BAD_REQUEST

# async def test_validate_question_fail(question, collection, mock_test_service_instance_bounded, mock_current_user,
#                                        data_for_tests, default_test_size):
#     test = mock_test_service_instance_bounded
#
#     failed_result = test.validate_question()
#
#     test.state += 1
#
#     assert result is None
#     assert isinstance(result, HTTPException)
#     assert result == HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

#
# @pytest.mark.asyncio
# def test_get_question_in_right_order_success(data_for_tests, mock_test_service_instance_bounded, mock_current_user, default_test_size):
#     user = mock_current_user.nick
#     test_instance = TestService.current_tests[user]
#     test_raw_data = data_for_tests
#
#     size = default_test_size
#     for id in range(size):
#         result = await TestService.get_question(user, id+1)
#         compare = test_raw_data[id]
#
#         test_instance.state += 1 # mock a part from tesrservice.submit_answer
#         assert isinstance(result, GetQuestion)
#         assert result.question == compare["question"]

#
# ----
# def validate_question(self,  question : UserResponse)-> None:
#         """
#         if the proper question was answered - initiates answer validation
#
#         :param question: UserResponse
#         :return: None
#         """
#
#         # true_ans = question.answers.ans_validation
#         # pass= self.clean_text()
#
#         test_question = self.questions[self.state - 1]
#         if test_question.question.id != question.chosen_question_id:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#
#         self.validate_answer(test_question, question)
#
#         # if self.clean_text(question.response) == self.clean_text(true_answers):
#         #     self.true_ans += 1 #if true add point to outcome


@pytest.mark.parametrize('question, collection', mock_user_responses_collection())
def test_validate_answer_cases(question, collection, mock_test_service_instance_bounded, mock_current_user, data_for_tests):
    #check 4 true answer i dla false
    test = mock_test_service_instance_bounded

    # for question in data_for_tests:
    # true answer - success
    check_before_score = test.true_ans
    test.validate_answer(test_question=get_AnsweredQuestion_schema(question), user_answer=collection['true_response'])
    check_after_score = test.true_ans
    assert check_before_score + 1 == check_after_score

    # false_response
    check_before_score = test.true_ans
    test.validate_answer(test_question=get_AnsweredQuestion_schema(question), user_answer=collection['false_response'])
    check_after_score = test.true_ans
    assert check_before_score == check_after_score

    # fake_response
    check_before_score = test.true_ans
    test.validate_answer(test_question=get_AnsweredQuestion_schema(question), user_answer=collection['nonexistent_response'])
    check_after_score = test.true_ans
    assert check_before_score == check_after_score



#
# @pytest.mark.asyncio
# async def test_random_questions_success(mock_async_session, default_test_size):
#     # Wywołanie metody `random_questions`
#     result = await TestService.random_questions(session=mock_async_session, test_size=default_test_size)
#
#     # Assert: wynik powinien być instancją TestService
#     assert isinstance(result, TestService)
#
#     # Assert: długość pytań odpowiada test_size
#     assert len(result.questions) == default_test_size
#
#     # Assert: pierwsze pytanie zawiera prawidłowe dane
#     first_question = result.questions[0]
#     assert first_question.question.id == 1
#     assert first_question.question.question == "Question 1"
#     assert len(first_question.answers) == 1
#     assert first_question.answers[0].answer == "Answer 1"
#     # assert first_question.answers[0].ans_validation is True
#
# @pytest.mark.asyncio
# async def test_mock_chain_calls(mock_async_session):
#     # Wywołanie metody random_questions
#     await TestService.random_questions(session=mock_async_session, test_size=5)
#
#     # Assert: Czy execute zostało wywołane?
#     mock_async_session.execute.assert_called_once()
#     # Assert: Czy scalars() zostało wywołane?
#     mock_async_session.execute.return_value.scalars.assert_called_once()
#     # Assert: Czy unique() zostało wywołane?
#     mock_async_session.execute.return_value.scalars.return_value.unique.assert_called_once()
#     # Assert: Czy all() zostało wywołane?
#     mock_async_session.execute.return_value.scalars.return_value.unique.return_value.all.assert_called_once()
#
# @pytest.mark.asyncio
# async def test_random_questions_success(mock_async_session, default_test_size, data_for_tests):
#     result = await TestService.random_questions(session=mock_async_session, test_size=default_test_size)
#
#     assert isinstance(result, TestService)
#     assert len(result.questions) == default_test_size
#
# #
# @pytest.mark.asyncio
# async def test_random_questions_success( mock_async_session, ):
#     @classmethod
#     async def random_questions(cls
#                                , session: AsyncSession
#                                , test_size: int
#                                # , user: User
#                                ) -> 'TestService':
#         """
#         Selects questions for db at random, and creates TestService instance for user
#
#         :param session : AsyncSession
#         :param test_size : int
#         :return: TestService
#         :raises HTTPException:
#             - 502 BAD GATEWAY in case of database error of any kind
#             - 404 NOT FOUND if for some reason there are more or less questions found in db then needed
#             - 500 INTERNAL SERVER ERROR if the retrieved data fails validation
#         """
#
#         try:
#             # select questions at random
#             result_dupl = await session.execute(
#                 select(Question)
#                 .order_by(func.random())  # Random question order
#                 .limit(test_size)  # Number of questions
#                 .options(joinedload(Question.answers))  # Eager loading answers
#             )
#             result = result_dupl.scalars().unique().all()
#
#         except SQLAlchemyError:
#             # would it be ok to add here wait_for_db()? -> to wait a moment for db before exception raise>?
#             raise HTTPException(status.HTTP_502_BAD_GATEWAY
#                                 , detail="Failed to get the test questions from db")
#
#         if len(result) != TEST_SIZE:
#             # eg. not enough questions in db
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
#                                 , detail="Test questions not found")
#
#         try:
#             # transform result for TestService purposes (validation based on Pydantic model
#             questions = [AnsweredQuestion(
#                 question=DbQuestion.model_validate(question),
#                 answers=random.sample(
#                     [DbAnswer.model_validate(answer) for answer in question.answers],
#                     len(question.answers))
#                 # as (at least in sample data) always the first answer is true - change order
#             ) for question in result]
#         except ValidationError:
#             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#         # Validation of new test
#         return cls(questions=questions)  # , user




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