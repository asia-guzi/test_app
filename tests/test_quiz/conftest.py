import random
import pytest
from app.quiz.services import TestService
import pytest
from app.quiz.services import TestService
from app.quiz.schemas import AnsweredQuestion, DbQuestion, DbAnswer
from app.quiz.models import Question, Answer



@pytest.fixture
def data_for_tests():
    questions_data = [
        {
            "id": 1,
            "question": "Question 1",
            "answers": [
                {"id": 1, "answer": "Answer 1", "question_id": 1, "ans_validation": True}
            ],
        },
        {
            "id": 2,
            "question": "Question 2",
            "answers": [
                {"id": 2, "answer": "Answer 2", "question_id": 2, "ans_validation": True}
            ],
        },
        {
            "id": 3,
            "question": "Question 3",
            "answers": [
                {"id": 3, "answer": "Answer 3", "question_id": 3, "ans_validation": True}
            ],
        },
        {
            "id": 4,
            "question": "Question 4",
            "answers": [
                {"id": 4, "answer": "Answer 4", "question_id": 4, "ans_validation": True}
            ],
        },
        {
            "id": 5,
            "question": "Question 5",
            "answers": [
                {"id": 5, "answer": "Answer 5", "question_id": 5, "ans_validation": True}
            ],
        },
    ]
    return questions_data

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
        AnsweredQuestion(
            question=DbQuestion.model_validate(
                {"id": data["id"], "question": data["question"]}
            ),
            answers=random.sample(
                [DbAnswer.model_validate(answer) for answer in data["answers"]],
                len(data["answers"]),
            ),
        )
        for data in questions_data
    ]
    test = TestService(questions=answered_questions)
    test.size=default_test_size # override default app TEST_SIZE varoable
    return test


@pytest.fixture
def mock_test_service_instance_bounded(mock_test_service_instance, mock_current_user):
    test = mock_test_service_instance
    nick = mock_current_user.nick
    TestService.current_tests[nick] = test

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

