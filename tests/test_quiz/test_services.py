import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError

from app.quiz.config import TEST_SIZE
from app.quiz.services import TestService
from app.quiz.models import Question
from app.quiz.schemas import DbQuestion, DbAnswer, AnsweredQuestion, GetQuestion
from datetime import datetime

import pytest
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import SQLAlchemyError
from app.quiz.services import TestService
from datetime import datetime
from tests.test_quiz.helpers import get_AnsweredQuestion_schema, mock_user_responses_collection, QUESTION_DATA

print(QUESTION_DATA)
print(len(QUESTION_DATA))

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



#casses - all wrong answers, all right answers, hal;f right answers
@pytest.mark.parametrize('points, result', [(0, 0), (len(QUESTION_DATA), 100), (len(QUESTION_DATA)//2, round(len(QUESTION_DATA)//2*100/len(QUESTION_DATA),2))])
@pytest.mark.asyncio
async def test_submit_answer_success(points, result, mock_db, mock_current_user, mock_test_service_instance_bounded, mock_async_session):


    test = mock_test_service_instance_bounded

    test.true_ans = points

    await TestService.submit_test(mock_current_user.nick, mock_async_session)


    print(mock_current_user.id)
    outcome = (mock_db[mock_current_user.id])['outcome']
    print(outcome)
    assert result == outcome


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


@pytest.mark.parametrize("test_size", [1, len(QUESTION_DATA)//2, len(QUESTION_DATA)])
@pytest.mark.asyncio
async def test_random_questions_success(test_size, mock_async_session, default_test_size):
    with patch("app.quiz.services.TEST_SIZE", test_size): #mock global test size vatiable

        result = await TestService.random_questions(session=mock_async_session, test_size=test_size)

        assert isinstance(result, TestService)
        assert len(result.questions) == test_size





# @pytest.mark.asyncio
# async def test_random_questions_not_enough_questions(self, mock_async_session):
