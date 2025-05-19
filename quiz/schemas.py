from pydantic import BaseModel
from typing import List

# from python_multipart.multipart import Field
from uuid import uuid4
from pydantic import BaseModel, Field
from sqlalchemy.sql.annotation import Annotated

from quiz.models import Question, Answer
from time import time
from .config import TEST_SIZE


class BaseQuestion(BaseModel):
    question: str

    """
    pozwala, aby Pydantic  model   mógł   być   używany   bezpośrednio   z   obiektami   ORM(np.SQLAlchemy).Oznacza
    to, że   możesz   tworzyć   instancje   modelu   Pydantic   na   podstawie   obiektów   ORM
    w   taki   sposób, jakby    pracowały   z   regularnymi   słownikami(dictionaries).   """
class IdOfQuestion(BaseModel):
    id: int #= Field(..., alias="id_q")  # "id" to alias
    """
    class IdOfQuestion(BaseModel):
    id: int
    
    
    
    class IdOfAnswer(BaseModel):
        id: int
    
    
    
    class UserResponse(IdOfQuestion, IdOfAnswer):
        pass
    
    ale grupuje mi id w jedno pole, a chcialam oba, a srednio moge smienic nazwe bo te pla maja sie mapowac do modeli orm z sql alchemy, no a najwyrazniej fastapi moze misc tylko jedno pole o takiej samej nazwie. co robvic?
    
    
    
    
    Masz rację, FastAPI i Pydantic (na którym bazuje) wymagają, aby pola w klasie Pydantic miały unikalne nazwy. Jeśli dziedziczysz po dwóch klasach (IdOfQuestion i IdOfAnswer), oba mają pole o nazwie id. W tym przypadku występuje konflikt nazw, ponieważ Pydantic nie wie, jak rozróżnić te pola.
    
    Rozwiązania:
    
    1. Zmienienie nazw pól w klasach podstawowych
    Jeśli masz kontrolę nad modelami ORM i możesz zaktualizować ich pola (zdejmując ten wymóg nazwiska id), przykładowo możesz dostosować nazwy pól bazowych, aby uniknąć konfliktu w dziedziczeniu:
    
    python
    
    
    class IdOfQuestion(BaseModel):
        question_id: int  # Zmieniona nazwa pola
    
    class IdOfAnswer(BaseModel):
        answer_id: int  # Zmieniona nazwa pola
    
    class UserResponse(IdOfQuestion, IdOfAnswer):
    pass
    
    ik tak zmiany aliasow nie pomogly, wiec ostatecznie reczie pola zdefiniowalam zeby sie nadpisalu
    """


class DbQuestion(BaseQuestion, IdOfQuestion):
    class Config:
        from_attributes = True

class BaseAnswer (BaseModel):
    answer: str



class IdOfAnswer(BaseModel):
    id: int #= Field(..., alias="id_a")  # "id" to alias


# class ValidatedAnswer(BaseAnswer):
#



class IdentifiedAnswer(BaseAnswer,IdOfAnswer):
    pass

class DbAnswer(IdentifiedAnswer):

    question_id: int
    ans_validation: bool

    class Config:
        from_attributes = True  # Pozwala mapować odpowiedzi i pytania z ORM


class GetQuestion(DbQuestion):
    response: list[IdentifiedAnswer] #list[str]




class UserResponse(BaseModel):
    chosen_question_id: int
    chosen_answer_id: int


class AnsweredQuestion(BaseModel):
    question: DbQuestion
    answers: List[DbAnswer]

    class Config:
        from_attributes = True  # Pozwala mapować odpowiedzi i pytania z ORM




#
# class TestSet(BaseModel):
#     questions: List[AnsweredQuestion]
#     size : int = TEST_SIZE
#     state : int = 1
#     true_ans = Field() 0
#     start_time = time()
#     #id: str = Field(default_factory=lambda: uuid4().hex) #indywidualne id zeby zidentyfikowac set uzytkownika
#     user_id : str
#

#
# class TestOutcome():
#
#
#     users_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     time_finish = Column(Time)
#     outcome =
#     user = relationship("User", back_populates="tests")

# class Test_output(Base):
#     __tablename__ = "test_outcomes"
#
#     id = Column(Integer, primary_key=True, autoincrement=True) #, index=True)
#     users_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     time_finish = Column(Time)
#     outcome = Column(Float, nullable=False) #number of crrect answers / all questions
#     user = relationship("User", back_populates="tests")
#
#



"""
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
# from users.model import User, Post
from pydantic import BaseModel
from datetime import datetime

#
#
# class Answered_question(BaseModel):
#     question: str
#     answer: str
#     answer_validation: bool = True
#
# class Output (BaseModel):
#     questions: int
#     correct_ans: int
#     date: datetime

"""