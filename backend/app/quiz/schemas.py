from typing import List
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class DbQuestion(BaseModel):
    # ConfigDict(from_attributes=True)

    id: int
    question: str

    class Config:
        from_attributes = True


class IdentifiedAnswer(BaseModel):
    id: int
    answer: str


class DbAnswer(IdentifiedAnswer):
    # ConfigDict(from_attributes=True)

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
    # ConfigDict(from_attributes=True)

    question: DbQuestion
    answers: List[DbAnswer]

    class Config:
        from_attributes = True


class TestOutcome(BaseModel):
    users_id: int
    end_time: datetime
    start_time: datetime
    outcome: float
