from pydantic import BaseModel
from typing import List

# from python_multipart.multipart import Field
from uuid import uuid4
from pydantic import BaseModel, Field

from quiz.models import Question, Answer
from time import time


class UserResponse(BaseModel):
    question_id:
    response_id: str


class TestQuestion(BaseModel):
    question_id:
    question: str
    response: List[str]


class TestSet(BaseModel):
    questions: List[TestQuestion] = None
    size = 20
    true_ans = Field() 0
    start_time = time()
    id: str = Field(default_factory=lambda: uuid4().hex) #indywidualne id zeby zidentyfikowac set uzytkownika


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