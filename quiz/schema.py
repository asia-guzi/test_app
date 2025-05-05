from pydantic import BaseModel

class UserResponse(BaseModel):
    question_id: str
    response_id: str

class TestQuestion(BaseModel):
    question: str
    response: str


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