from quiz.models import Question, Answer
from quiz.schemas import TestSet
from typing import List

class TestService:

    def __init__(self, test_set: TestSet):
        self.test = TestSet


    @staticmethod
    async def get_questions(test_size) ->  List[Question]:
        '''
        I/O operation, async function to get questions from db
        :return:
        '''
        # sync by byłp
        #         (  # zamienic na execute query i doda
        #             session.query(Question)
        #             .options(joinedload(Question.answers))  # need a complet of Q + A
        #             .order_by(func.random())  # select questions from base at random
        #             .limit(test_size)
        #             .all())
        result = await session.execute(
            select(Question)
            .options(joinedload(Question.answers))  # Eager loading answers
            .order_by(func.random())  # Random question order
            .limit(test_size)  # Number of questions
        )
        questions = result.scalars().all()  # Pobierz wyniki jako lista obiektów
        return questions


    @classmethod
    async def get_test(cls, ):

        test = cls(test_size)
        test.questions = await get_questions(test.size)

        return test




    def validate_answer(self, question, answer):
        '''
        validation of user answer
        :param question:
        :param answer:
        :return:
        '''
        if validation true:
            self.true_ans +=1

        pass

    def submit_test(self):
        '''
        function to count the outcome and save it into db
        :return:
        '''
        pass


class QuestionService():
    # Code above omitted 👆

    @
    async def create_hero(hero: Hero, session: SessionDep) -> Hero:
        '''https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-hero'''
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero

    # Code above omitted 👆

    @app.get("/heroes/")
    def read_heroes(
            session: SessionDep,
            offset: int = 0,
            limit: Annotated[int, Query(le=100)] = 100,
    ) -> list[Hero]:
        heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
        return heroes

    # Code above omitted 👆

    @app.delete("/heroes/{hero_id}")
    def delete_hero(hero_id: int, session: SessionDep):
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        session.delete(hero)
        session.commit()
        return {"ok": True}