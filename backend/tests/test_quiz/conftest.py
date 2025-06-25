import pytest
from app.quiz.services import TestService
from app.quiz.models import Question, Answer
from app.quiz.schemas import UserResponse
from tests.test_quiz.helpers import get_AnsweredQuestion_schema
from unittest.mock import patch, Mock, AsyncMock


from tests.test_quiz.helpers import QUESTION_DATA


@pytest.fixture
def data_for_tests():
    return QUESTION_DATA


@pytest.fixture
def mock_validate_answer():
    with patch.object(TestService, "validate_answer", return_value=None) as mock_method:
        yield mock_method


@pytest.fixture
def default_test_size(data_for_tests):
    """
    mock test size
    """

    return len(data_for_tests)  # == len of questions_data im mock_test_service


@pytest.fixture
def mock_test_service_instance(data_for_tests, default_test_size):
    """
    deliver TestService instance
    """
    questions_data = data_for_tests

    answered_questions = [get_AnsweredQuestion_schema(data) for data in questions_data]
    test = TestService(questions=answered_questions)
    test.size = default_test_size  # override default app TEST_SIZE varoable
    return test


@pytest.fixture
def mock_user_true_responses():
    """
    generator of set of user's collections for each question in test set
    """
    responses = []
    for question in QUESTION_DATA:

        question_id = question["id"]

        for answer in question["answers"]:
            if answer["ans_validation"] == True:
                responses.append(
                    UserResponse(
                        chosen_question_id=question_id, chosen_answer_id=answer["id"]
                    )
                )
    return responses


@pytest.fixture
def mock_user_true_false():
    """
    generator of set of user's collections for each question in test set
    """
    responses = []
    for question in QUESTION_DATA:

        question_id = question["id"]
        responses.append(
            UserResponse(chosen_question_id=question_id + 1, chosen_answer_id=1)
        )
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
def mock_db():
    mock_db = {}
    return mock_db


@pytest.fixture
def mock_db_output(data_for_tests):

    orm_questions = []

    for q in data_for_tests:

        answers = [
            Answer(
                id=ans["id"],
                answer=ans["answer"],
                question_id=ans["question_id"],
                ans_validation=ans["ans_validation"],
            )
            for ans in q["answers"]
        ]

        # Tworzymy obiekt Question z przypisanymi odpowiedziami
        question = Question(
            id=q["id"],
            question=q["question"],
            answers=answers,  # Powiązujemy odpowiedzi z pytaniem (relacja ORM)
        )

        orm_questions.append(question)

    return orm_questions


@pytest.fixture
def mock_async_session(mocker, mock_db_output, mock_db):
    session = Mock()
    mock_db = mock_db

    def add(instance):

        mock_db[instance.users_id] = {
            "end_time": instance.end_time,
            "start_time": instance.start_time,
            "outcome": instance.outcome,
        }

    session.add.side_effect = add

    async def commit():
        pass

    session.commit = AsyncMock(side_effect=commit)

    async def refresh(instance):
        pass

    session.refresh = AsyncMock(side_effect=refresh)

    async def execute(instance, *args, **kwargs):
        test_size = instance._limit_clause.value

        result = mock_db_output[:test_size]

        class MockResult:

            def __init__(self, data):
                self.data = data

            def scalars(self):
                return self

            def unique(self):
                return self

            def all(self):
                return self

            def __len__(self):
                return len(self.data)

            def __iter__(self):
                return iter(self.data)

        return MockResult(result)

    session.execute = AsyncMock(side_effect=execute)

    return session
