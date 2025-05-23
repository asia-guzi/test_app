from app.quiz.models import Question, TestResult
from app.quiz.schemas import AnsweredQuestion, UserResponse, DbAnswer, DbQuestion, GetQuestion, IdentifiedAnswer, TestOutcome
from .config import TEST_SIZE
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from fastapi.responses import RedirectResponse
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
        return test



    @classmethod
    async def get_question(cls, user : str, id: int):

        test = cls.current_tests[user]

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
        true_id = next(answer.id for answer in test_question.answers if answer.ans_validation)

        if true_id == user_answer.chosen_answer_id:
            #raise outcome if true answer
            self.true_ans += 1

    def validate_question(self,  question : UserResponse):
        """
        validation of user answer
        :param question:
        :return:
        """
        #
        # true_ans = question.answers.ans_validation
        # pass= self.clean_text()
        test_question = self.questions[self.state - 1]
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


        test.validate_question(question)

        test.state += 1

        if id < test.size: #not lastr question
            # return RedirectResponse(f'/question/{id + 1}')
            return RedirectResponse(f'/frontend/question/{id + 1}',
                                    status_code=303)  # Wymusza metodę GET podczas przekierowania

        elif id == test.size: #last question
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


        test = cls.current_tests[user]
        outcome = round(test.true_ans / test.size * 100, 2)

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
