# users/users.py
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, PrimaryKeyConstraint
from db.config import async_engine
from sqlalchemy.orm import DeclarativeBase #,


#base for the users
class Base(DeclarativeBase):
    pass





# Create Question model (~ row in db)
class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(100), nullable=False)
    answers = relationship("Answer", back_populates="questions")  # one -> many (a)
    #technical requirements of the relationship checked by check_valid_answers trigger





# each answer is connected to particular question, has attribute indicating a correct answer
class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String(100), nullable=False)
    ans_validation = Column(Boolean, nullable=False, default=False)
    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="answers")   # many -> one (q)
    # technical requirements of the relationship checked by check_valid_answers trigger
#
#
# class Pupil(Base):
#     __tablename__ = "pupils"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name
#     surname
#     birth date
#     access do start test i do wynik test przydzielonego przez teacher
#
#
# class Teacher(Pupil):
#     __tablename__ = "teachers"
#
#
#
# class Test_output(Base):
#     __tablename__ = "test_outcomes"
#
#     id = Column(Integer, primary_key=True, index=True)
#     pupil_id = Column(Integer, ForeignKey("pupils.id"))
#     time_finish =
#     outcome = #number of crrect answers
#


