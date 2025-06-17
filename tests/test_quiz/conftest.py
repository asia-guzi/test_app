import random
import pytest
from app.quiz.services import TestService
import pytest
from app.quiz.services import TestService
from app.quiz.models import Question, Answer
from app.quiz.schemas import UserResponse
from tests.test_quiz.helpers import get_AnsweredQuestion_schema
from unittest.mock import patch


from tests.test_quiz.helpers import QUESTION_DATA

@pytest.fixture
def data_for_tests():
    return QUESTION_DATA


@pytest.fixture
def mock_validate_answer():
    with patch.object(TestService, 'validate_answer', return_value=None) as mock_method:
        yield mock_method


@pytest.fixture
def default_test_size(data_for_tests):
    """
    mock test size
    """
    return len(data_for_tests) # == len of questions_data im mock_test_service


@pytest.fixture
def mock_test_service_instance(data_for_tests, default_test_size):
    """
    deliver TestService instance
    """
    # Symulacja pytań, jakby pochodziły z funkcji random_questions
    questions_data = data_for_tests

    # Generujemy AnsweredQuestion na podstawie danych
    answered_questions = [
        get_AnsweredQuestion_schema(data)
        for data in questions_data
    ]
    test = TestService(questions=answered_questions)
    test.size=default_test_size # override default app TEST_SIZE varoable
    return test


@pytest.fixture
def mock_user_true_responses():
    """
    generator of set of user's collections for each question in test set
    """
    responses = []
    for question in QUESTION_DATA:

        question_id = question['id']

        for answer in question['answers']:
            if answer['ans_validation'] == True:
               responses.append(UserResponse(
                    chosen_question_id = question_id
                    , chosen_answer_id = answer['id']
                ))
    return responses



@pytest.fixture
def mock_user_true_false():
    """
    generator of set of user's collections for each question in test set
    """
    responses = []
    for question in QUESTION_DATA:

        question_id = question['id']
        responses.append(UserResponse(
            chosen_question_id = question_id  + 1
            , chosen_answer_id = 1
            ))
    return responses



@pytest.fixture
def mock_test_service_instance_bounded(mock_test_service_instance, mock_current_user):
    test = mock_test_service_instance
    nick = mock_current_user.nick
    TestService.current_tests[nick] = test
    return test


@pytest.fixture
def mock_random_questions(mocker, mock_test_service_instance):
    """
    imitate TestService.random_questions()
    """
    mock = mocker.patch.object(TestService, "random_questions")
    mock.return_value = mock_test_service_instance  # use mock_test_service
    return mock

@pytest.fixture
def mock_async_session(mocker, data_for_tests):
    questions = [
        Question(
            id=data["id"],
            question=data["question"],
            answers=[
                Answer(
                    id=answer["id"],
                    answer=answer["answer"],
                    question_id=answer["question_id"],
                    ans_validation=answer["ans_validation"],
                )
                for answer in data["answers"]
            ],
        )
        for data in data_for_tests
    ]

    mock_execute = mocker.AsyncMock()
    mock_scalars = mocker.MagicMock()
    mock_unique = mocker.MagicMock()

    mock_unique.all.return_value = questions
    mock_scalars.unique.return_value = mock_unique
    mock_execute.scalars.return_value = mock_scalars

    mock_session = mocker.MagicMock()
    mock_session.execute.return_value = mock_execute
    return mock_session

# # Deliver TestService instance
# @pytest.fixture
# def mock_test_service():
#     with patch.object(TestService, 'create_test', new_callable=AsyncMock) as mock_create_test, \
#             patch.object(TestService, 'get_question', new_callable=AsyncMock) as mock_get_question, \
#             patch.object(TestService, 'submit_answer', new_callable=AsyncMock) as mock_submit_answer, \
#             patch.object(TestService, 'submit_test', new_callable=AsyncMock) as mock_submit_test:
#         yield {
#             'create_test': mock_create_test,
#             'get_question': mock_get_question,
#             'submit_answer': mock_submit_answer,
#             'submit_test': mock_submit_test
#         }
#
# # Fixture: Mockowanie zależności get_session
# @pytest.fixture
# def override_get_session(mock_session):
#     app.dependency_overrides[get_session] = lambda: mock_session
#     yield
#     app.dependency_overrides.pop(get_session)

