from pydantic import ValidationError

from backend.app.quiz.models import Question, TestResult
from backend.app.quiz.schemas import (
    AnsweredQuestion,
    UserResponse,
    DbAnswer,
    DbQuestion,
    GetQuestion,
    IdentifiedAnswer,
    TestOutcome,
)
from backend.app.quiz.config import TEST_SIZE
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from fastapi.responses import RedirectResponse
from datetime import datetime
import random
from typing import Dict, Union


class TestService:
    __test__ = False  # pytest tried to performn tests here

    current_tests = {}

    def __init__(self, questions):  # user: User):
        self.questions = questions
        self.size = TEST_SIZE
        self.state = 1
        self.true_ans = 0
        self.start_time = datetime.now()
        self.test_user = 1  # User

    @classmethod
    async def random_questions(
        cls,
        session: AsyncSession,
        test_size: int,
    ) -> "TestService":
        """
        Selects questions for db at random, and creates TestService instance for user

        :param session : AsyncSession
        :param test_size : int
        :return: TestService
        :raises HTTPException:
            - 502 BAD GATEWAY in case of database error of any kind
            - 404 NOT FOUND if for some reason there are more or less questions found in db then needed
            - 500 INTERNAL SERVER ERROR if the retrieved data fails validation
        """

        try:
            # select questions at random
            result_dupl = await session.execute(
                select(Question)
                .order_by(func.random())  # Random question order
                .limit(test_size)  # Number of questions
                .options(joinedload(Question.answers))  # Eager loading answers
            )
            result = result_dupl.scalars().unique().all()
            print(result, "result")
        except SQLAlchemyError:
            raise HTTPException(
                status.HTTP_502_BAD_GATEWAY,
                detail="Failed to get the test questions from db",
            )

        if len(result) != TEST_SIZE:
            # eg. not enough questions in db
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Test questions not found"
            )

        try:

            # transform result for TestService purposes (validation based on Pydantic model
            questions = [
                AnsweredQuestion(
                    question=DbQuestion.model_validate(question),
                    answers=random.sample(
                        [
                            DbAnswer.model_validate(answer)
                            for answer in question.answers
                        ],
                        len(question.answers),
                    ),
                )
                for question in result
            ]
        except ValidationError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Validation of new test
        return cls(questions=questions)  # , user

    @classmethod
    async def create_test(cls, user: str, session: AsyncSession) -> "TestService":
        """
        Starts the process of TestService instance creation
        and binds particular TestService instance with user
        (by adding to class dict current_tests)

        :param user : str
        :param session : AsyncSession
        :return: TestService
        """
        test = await cls.random_questions(session=session, test_size=TEST_SIZE)
        cls.current_tests[user] = test
        return test

    @classmethod
    async def get_question(
        cls, user: str, id: int
    ) -> Union[GetQuestion, RedirectResponse, HTTPException]:

        test = cls.current_tests[user]

        if id != test.state:
            # if user tries to skip / go back to questoion
            error_message = "An attempt to skip or go back to question is not allowed"
            return RedirectResponse(url=f"/question/{test.state}?error={error_message}")

        if id <= test.size:
            # id is not out of range
            test_question = test.questions[test.state - 1]
            return GetQuestion(
                # question=BaseQuestion.model_validate((test_question.question).question),
                id=test_question.question.id,
                question=test_question.question.question,
                response=[
                    IdentifiedAnswer.model_validate(answer)
                    for answer in test_question.answers
                ],
            )

    def validate_answer(
        self, test_question: AnsweredQuestion, user_answer: UserResponse
    ) -> None:
        """
        if user chose true answer, raises test outcome by 1 point
        (raises counter of true_ans in TestService instance)

        :param test_question: AnsweredQuestion
        :param user_answer: UserResponse
        :return: None
        """
        # generator - as question has 1 true answer (usually first in list),
        # if answer is true <=> no point to look forward
        true_id = next(
            answer.id for answer in test_question.answers if answer.ans_validation
        )

        # if user chose true answer, raise test outcome by 1 point
        if true_id == user_answer.chosen_answer_id:
            # raise outcome if true answer
            self.true_ans += 1

    def validate_question(self, question: UserResponse) -> None:
        """
        if the proper question was answered - initiates answer validation

        :param question: UserResponse
        :return: None
        """

        test_question = self.questions[self.state - 1]

        if test_question.question.id != question.chosen_question_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        self.validate_answer(test_question, question)

    @classmethod
    def submit_answer(
        cls, user: str, id: int, question: UserResponse
    ) -> Union[RedirectResponse, HTTPException]:
        """
        initiates process of processing of particular question answered by user

        :param user: str
        :param id: int
        :param question : UserResponse
        """
        test = cls.current_tests[user]

        if id != test.state:
            # if user tries to skip / go back to questoion

            error_message = "An attempt to skip or go back to question is not allowed"

            # redirect to proper question
            # return RedirectResponse(url=f"/question/{test.state}?error={error_message}")
            return RedirectResponse(
                f"/frontend/question/{test.state}?error={error_message}",
                status_code=303,
            )

        # if question is of correct order, validate question and answer
        test.validate_question(question)

        # after question is processed - move to the next question (by changing test.state in TestService instance)
        test.state += 1

        if id < test.size:
            # branch to follow if current question is NOT the last one of test
            # redirects to url of next question

            # return RedirectResponse(f'/question/{id + 1}')
            return RedirectResponse(f"/frontend/question/{id + 1}", status_code=303)

        elif id == test.size:
            # branch to follow if current question IS the last one of test

            # redirects to url to handle test ending and submission
            return RedirectResponse(url="/end_test", status_code=303)
        else:  # test id out of range
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    @classmethod
    async def submit_test(cls, user: str, session: AsyncSession) -> Dict:
        """
        function to count the outcome and save it into db

        :param user: str
        :param session : AsyncSession
        :return: Dict
        :raises HTTPException:
            - 502 BAD GATEWAY in case of database error of any kind
            - 500 INTERNAL SERVER ERROR if the retrieved data fails validation
        """

        # get TestService instance bind with the user
        test = cls.current_tests[user]

        # count the test outcome based on true answers amount
        outcome = round(test.true_ans / test.size * 100, 2)

        try:
            # validate data based on schema
            test_result = TestOutcome(
                users_id=test.test_user,  # .id
                end_time=datetime.now(),
                start_time=test.start_time,
                outcome=outcome,
            )
        except ValidationError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # create a row
        to_db = TestResult(
            users_id=test_result.users_id,
            end_time=test_result.end_time,
            start_time=test_result.start_time,
            outcome=test_result.outcome,
        )

        try:
            session.add(to_db)
            await session.commit()
            await session.refresh(to_db)
        except SQLAlchemyError:
            # would it be ok to add here wait_for_db()? -> to wait a moment for db before exception raise>?
            raise HTTPException(
                status.HTTP_502_BAD_GATEWAY, detail="Failed to save the test outcome"
            )

        return {"message": f"test finished, your grade is {outcome} %"}
