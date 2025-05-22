from quiz.models import Question, Answer, TestResult
from quiz.schemas import AnsweredQuestion, UserResponse, DbAnswer, DbQuestion, GetQuestion, BaseAnswer, BaseQuestion, IdentifiedAnswer, TestOutcome
from .config import TEST_SIZE
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from fastapi.responses import RedirectResponse, JSONResponse
import re
from datetime import datetime
import random


class TestService:

    current_tests = {}

    def __init__(self,
                 questions): # user: User):
        self.questions = questions
        self.size = TEST_SIZE
        self.state = 1
        self.true_ans = 0
        self.start_time = datetime.now()
        self.test_user = 1 # User
        #self.id = test_set.id  # indywidualne id zeby zidentyfikowac set uzytkownika
        #self.user_id = test_set.user_id - user as kwy in dict


    @classmethod
    async def random_questions(cls
                            , session : AsyncSession
                            , test_size
                               #, user: User
                            ) ->  'TestService':
        """
        I/O operation, async function to get questions from db
        :return:
        """

        result_dupl = await session.execute(
            select(Question)
            .order_by(func.random())  # Random question order
            .limit(test_size)  # Number of questions
            .options(joinedload(Question.answers))  # Eager loading answers

        )

        # result = result_dupl.unique() -> tyu zapytanie bylo nieprzetworzone wiec nie dzoialala konwersja typow
        result = result_dupl.scalars().unique().all()

        # sync by byłp
        #         (  # zamienic na execute query i doda
        #             session.query(Question)
        #             .options(joinedload(Question.answers))  # need a complet of Q + A
        #             .order_by(func.random())  # select questions from base at random
        #             .limit(test_size)
        #             .all())

        # Bezpośrednia konwersja ORM -> Pydantic przy pomocy from_orm() - mozliwa dzieki  class Config:
        #         orm_mode = True  # Pozwala mapować odpowiedzi i pytania z ORM
        # questions = [AnsweredQuestion.model_validate(q) for q in result.scalars().all()]

        questions = [ AnsweredQuestion(
            question=DbQuestion.model_validate(question),
            #answers=[DbAnswer.model_validate(answer) for answer in question.answers]
            #in db 1. question is true - need to replace it at random. random sample to
            #get a copy, and not to manipulate src data (like list.shuffle would)- 4 app logic to find true easier each time
            answers=random.sample(
                [DbAnswer.model_validate(answer) for answer in question.answers],
                len(question.answers)  # Losowe przemieszanie odpowiedzi
        )
        )
        for question in result]

        # questions = [AnsweredQuestion.model_validate(q).model_dump() for q in result.scalars().all()]


        #Validation of new test
        # set_for_one_test = TestSet(test_set=questions)  # Pobierz wyniki jako lista obiektów
        return cls(questions=questions) #, user

    @classmethod
    async def create_test(cls, user: str, session: AsyncSession):

        test = await cls.random_questions(session=session,
                                       test_size=TEST_SIZE)
        cls.current_tests[user] = test
          # test.questions = await get_questions(test.size)
          #
        print(test.questions, '\n TESTS')
        return test



    @classmethod
    async def get_question(cls, user : str, id: int):

        test = cls.current_tests[user]
        print(F'USER OF TEST {user} \n QUESTION ID {id}, \n QUESTION {test.questions[test.state -1]}')

        #change it to separate verify_test_state(self)
        if id != test.state:
            #if user tries to skip / go back to questoion
            error_message = "An attempt to skip or go back to question is not allowed"
            return RedirectResponse(url=f"/question/{test.state}?error={error_message}")


        if id <= test.size:  # id not out of range
            test_question = test.questions[test.state -1]
            return    GetQuestion(
                #question=BaseQuestion.model_validate((test_question.question).question),
                id=test_question.question.id,
                question=test_question.question.question,
                response=[IdentifiedAnswer.model_validate(answer) for answer in test_question.answers]
                #które by było lepsze, bo zakomwentowae na pewno jest jsonowe bardziej
                #response=[answer.answer for answer in test_question.answers]
            )

        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # @staticmethod
    # def clean_text(text):
    #     # Najpierw usuń białe znaki (spacje, tabulatory itp.)
    #     text = text.strip()
    #     # Konwersja na lowercase
    #     text = text.lower()
    #     # Usunięcie wszystkiego poza literami i cyframi
    #     text = re.sub(r'[^\w]', '', text)
    #     return text

    def validate_answer(self, test_question: AnsweredQuestion, user_answer: UserResponse):

        #generator - zeby mi znalazł prawdziwą odp i przestał szukać
        print('validate_answer')
        true_id = next(answer.id for answer in test_question.answers if answer.ans_validation)
        print('true_id', true_id)
        print('true_ans' , user_answer.chosen_answer_id)
        if true_id == user_answer.chosen_answer_id:
            #raise outcome if true answer
            self.true_ans += 1
            print('true_ans in ', self.true_ans )

    def validate_question(self,  question : UserResponse):
        """
        validation of user answer
        :param question:
        :return:
        """
        print('validate_question')
        #
        # true_ans = question.answers.ans_validation
        # pass= self.clean_text()
        test_question = self.questions[self.state - 1]
        print(test_question.question.id , question.chosen_question_id)
        if test_question.question.id != question.chosen_question_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        self.validate_answer(test_question, question)

        # if self.clean_text(question.response) == self.clean_text(true_answers):
        #     self.true_ans += 1 #if true add point to outcome

    @classmethod
    def submit_answer(cls, user: str, id: int, question : UserResponse):

        test = cls.current_tests[user]



        # change it to separate verify_test_state(self)
        if id != test.state:
            # if user tries to skip / go back to questoion
            error_message = "An attempt to skip or go back to question is not allowed"
            return RedirectResponse(url=f"/question/{test.state}?error={error_message}")
        print(f'bf: id {id}, state {test.state }')


        test.validate_question(question)

        test.state += 1

        print(f'af: id {id}, state {test.state }')
        if id < test.size: #not lastr question
            print('ok')
            # return RedirectResponse(f'/question/{id + 1}')
            return RedirectResponse(f'/frontend/question/{id + 1}',
                                    status_code=303)  # Wymusza metodę GET podczas przekierowania

        elif id == test.size: #last question
            print('end')
            print(test)
            return RedirectResponse(url='/end_test',  status_code=303) # GET#, status_code=307)  # Zachowuje metodę POST)
            # return JSONResponse(content={"redirect_url": "/end_test"}, status_code=200)
            #json response, bo jak bylo redirect, to z jakiegos powodu metoda wywoływała sie 2 razy i 2 razy zapisywała do db
        else: # out of range
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # return test

    @classmethod
    async def submit_test(cls, user, session : AsyncSession):
        """
        function to count the outcome and save it into db
        :return:
        """

        print ('bf test')

        print(cls.current_tests)
        test = cls.current_tests[user]
        print('bf outcome')
        outcome = round(test.true_ans / test.size * 100, 2)
        #pass the submision into db

        test_result =    TestOutcome(   users_id = test.test_user #.id
                                        , end_time = datetime.now()
                                    , start_time = test.start_time
                                    ,outcome = outcome)
        to_db = TestResult(
                users_id = test_result.users_id
                ,end_time = test_result.end_time
                ,start_time = test_result.start_time
                ,outcome = test_result.outcome)


        session.add(to_db)
        await session.commit()
        await session.refresh(to_db)

        return {"message": f"test finished, your grade is {outcome} %"}

# class QuestionService():
    # Code above omitted 👆
    #
    # @
    # async def create_hero(hero: Hero, session: SessionDep) -> Hero:
    #     """https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-hero
    #
    #     https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
    #     async_scoped_session includes proxy behavior similar to that of scoped_session, which means it can be treated as a AsyncSession directly, keeping in mind that the usual await keywords are necessary, including for the async_scoped_session.remove() method:
    #
    #     async def some_function(some_async_session, some_object):
    #     # use the AsyncSession directly
    #     some_async_session.add(some_object)
    #
    #     # use the AsyncSession via the context-local proxy
    #     await AsyncScopedSession.commit()
    #
    #     # "remove" the current proxied AsyncSession for the local context
    #     await AsyncScopedSession.remove()
    #     """
    #     await  session.add(hero)
    #     session.commit()
    #     await session.refresh(hero)
    #     return hero
#
#     # Code above omitted 👆
#
#     @app.get("/heroes/")
#     def read_heroes(
#             session: SessionDep,
#             offset: int = 0,
#             limit: Annotated[int, Query(le=100)] = 100,
#     ) -> list[Hero]:
#         heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
#         return heroes
#
#     # Code above omitted 👆
#
#     @app.delete("/heroes/{hero_id}")
#     def delete_hero(hero_id: int, session: SessionDep):
#         hero = session.get(Hero, hero_id)
#         if not hero:
#             raise HTTPException(status_code=404, detail="Hero not found")
#         session.delete(hero)
#         session.commit()
#         return {"ok": True}