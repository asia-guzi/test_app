from typing import List
from pydantic import BaseModel
from datetime import datetime


class BaseQuestion(BaseModel):
    question: str


class IdOfQuestion(BaseModel):
    id: int


class DbQuestion(BaseQuestion, IdOfQuestion):
    class Config:
        from_attributes = True


class BaseAnswer(BaseModel):
    answer: str


class IdOfAnswer(BaseModel):
    id: int


class IdentifiedAnswer(BaseAnswer, IdOfAnswer):
    pass


class DbAnswer(IdentifiedAnswer):
    question_id: int
    ans_validation: bool

    class Config:
        from_attributes = True


class GetQuestion(DbQuestion):
    response: list[IdentifiedAnswer]  # list[str]


class UserResponse(BaseModel):
    chosen_question_id: int
    chosen_answer_id: int


class AnsweredQuestion(BaseModel):
    question: DbQuestion
    answers: List[DbAnswer]

    class Config:
        from_attributes = True


class TestOutcome(BaseModel):
    users_id: int
    end_time: datetime
    start_time: datetime
    outcome: float
