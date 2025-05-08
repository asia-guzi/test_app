# users/users.py
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float, Integer, String, ForeignKey, Boolean, Time, PrimaryKeyConstraint
from db.config import async_engine
from db.config import Base
from users.models import User





# Create Question model (~ row in db)
class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True) #, index=True)
    question = Column(String(100), nullable=False)
    answers = relationship("Answer", back_populates="questions")  # one -> many (a)
    #technical requirements of the relationship checked by check_valid_answers trigger





# each answer is connected to particular question, has attribute indicating a correct answer
class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, autoincrement=True) #, index=True)
    answer = Column(String(100), nullable=False)
    ans_validation = Column(Boolean, nullable=False, default=False)
    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="answers")   # many -> one (q)
    # technical requirements of the relationship checked by check_valid_answers trigger



class Test_output(Base):
    __tablename__ = "test_outcomes"

    id = Column(Integer, primary_key=True, autoincrement=True) #, index=True)
    users_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    time_finish = Column(Time)
    outcome = Column(Float, nullable=False) #number of crrect answers / all questions
    user = relationship("User", back_populates="tests")



