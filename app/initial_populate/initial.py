import sys
import os

# Dodanie folderu nadrzędnego (`../`) do sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.config import async_engine, async_session, Base
from app.quiz.models import Question, Answer
from app.users.models import User
# from db.triggers import upgrade
from app.users.services import AccessServices
from sqlalchemy.future import select
import asyncio
from .models import DbCreated
from datetime import datetime
from sqlalchemy.exc import OperationalError


async def main():
    if not await is_initialized():
        await create_db()
        #upgrade()
        await insert_data()
        await insert_user('user', 'user')
        await mark_as_initizlized()

async def is_initialized():
    """
    returns true if db is created and initialized, else false
    """
    async with async_session() as session:
        try:
            query = select(DbCreated).order_by(DbCreated.creation_date.desc()).limit(1)
            result = await session.execute(query)
            flag = result.scalars().first()
            return False if flag is None else flag #if no record <=> false

        except OperationalError:
            #table does not yet exist
            return False

async def mark_as_initizlized():
    async with async_session() as session:
        try:
           session.add(DbCreated( creation_flag = True
                        ,creation_date =  datetime.now()))
           await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Error during flag creation: {e}")
async def create_db():
    """
    to create tables
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Insert questions and answers
async def insert_data():
    # Questions to insert
    questions = [
        {"question": "What is 1 + 1?", "answers": [("2", True), ("3", False), ("4", False), ("5", False)]},
        {"question": "What is 2 + 3?", "answers": [("5", True), ("4", False), ("6", False), ("7", False)]},
        {"question": "What is 5 - 2?", "answers": [("3", True), ("4", False), ("2", False), ("5", False)]},
        {"question": "What is 3 * 2?", "answers": [("6", True), ("5", False), ("7", False), ("8", False)]},
        {"question": "What is 10 - 4?", "answers": [("6", True), ("7", False), ("8", False), ("5", False)]},
        {"question": "What is 7 + 3?", "answers": [("10", True), ("11", False), ("12", False), ("9", False)]},
        {"question": "What is 6 / 2?", "answers": [("3", True), ("2", False), ("4", False), ("5", False)]},
        {"question": "What is 4 * 2?", "answers": [("8", True), ("6", False), ("9", False), ("7", False)]},
        {"question": "What is 9 - 5?", "answers": [("4", True), ("3", False), ("5", False), ("6", False)]},
        {"question": "What is 8 + 1?", "answers": [("9", True), ("10", False), ("8", False), ("11", False)]},
        {"question": "What is 10 / 2?", "answers": [("5", True), ("4", False), ("6", False), ("7", False)]},
        {"question": "What is 5 + 5?", "answers": [("10", True), ("11", False), ("12", False), ("9", False)]},
        {"question": "What is 3 + 7?", "answers": [("10", True), ("9", False), ("8", False), ("11", False)]},
        {"question": "What is 20 - 10?", "answers": [("10", True), ("9", False), ("11", False), ("8", False)]},
        {"question": "What is 6 * 3?", "answers": [("18", True), ("17", False), ("19", False), ("15", False)]},
        {"question": "What is 2 + 2?", "answers": [("4", True), ("5", False), ("3", False), ("6", False)]},
        {"question": "What is 3 * 3?", "answers": [("9", True), ("8", False), ("10", False), ("7", False)]},
        {"question": "What is 12 / 4?", "answers": [("3", True), ("2", False), ("4", False), ("5", False)]},
        {"question": "What is 15 - 5?", "answers": [("10", True), ("9", False), ("11", False), ("8", False)]},
        {"question": "What is 7 + 5?", "answers": [("12", True), ("11", False), ("13", False), ("10", False)]},
        {"question": "What is 1 + 0?", "answers": [("1", True), ("0", False), ("2", False), ("3", False)]},
        {"question": "What is 8 * 1?", "answers": [("8", True), ("7", False), ("9", False), ("6", False)]},
        {"question": "What is 10 - 7?", "answers": [("3", True), ("4", False), ("2", False), ("5", False)]},
        {"question": "What is 6 + 4?", "answers": [("10", True), ("11", False), ("9", False), ("12", False)]},
        {"question": "What is 12 - 6?", "answers": [("6", True), ("5", False), ("7", False), ("4", False)]},
        {"question": "What is 4 + 4?", "answers": [("8", True), ("9", False), ("7", False), ("6", False)]},
        {"question": "What is 2 * 5?", "answers": [("10", True), ("9", False), ("11", False), ("8", False)]},
        {"question": "What is 14 / 2?", "answers": [("7", True), ("6", False), ("8", False), ("5", False)]},
        {"question": "What is 9 + 2?", "answers": [("11", True), ("10", False), ("12", False), ("13", False)]},
        {"question": "What is 5 * 2?", "answers": [("10", True), ("11", False), ("9", False), ("12", False)]},
        {"question": "What is 4 - 1?", "answers": [("3", True), ("2", False), ("4", False), ("5", False)]},
        {"question": "What is 0 + 7?", "answers": [("7", True), ("6", False), ("8", False), ("9", False)]},
        {"question": "What is 3 * 4?", "answers": [("12", True), ("11", False), ("13", False), ("10", False)]},
        {"question": "What is 16 / 4?", "answers": [("4", True), ("3", False), ("5", False), ("6", False)]},
        {"question": "What is 8 - 4?", "answers": [("4", True), ("3", False), ("5", False), ("6", False)]},
        {"question": "What is 6 + 6?", "answers": [("12", True), ("11", False), ("13", False), ("10", False)]},
        {"question": "What is 18 / 3?", "answers": [("6", True), ("5", False), ("7", False), ("4", False)]},
        {"question": "What is 10 + 5?", "answers": [("15", True), ("14", False), ("16", False), ("13", False)]},
        {"question": "What is 7 - 1?", "answers": [("6", True), ("5", False), ("7", False), ("4", False)]},
        {"question": "What is 4 + 3?", "answers": [("7", True), ("6", False), ("8", False), ("5", False)]},
        {"question": "What is 5 * 3?", "answers": [("15", True), ("16", False), ("14", False), ("13", False)]},
        {"question": "What is 15 / 5?", "answers": [("3", True), ("2", False), ("4", False), ("5", False)]},
        {"question": "What is 10 - 9?", "answers": [("1", True), ("2", False), ("0", False), ("3", False)]},
        {"question": "What is 3 + 2?", "answers": [("5", True), ("4", False), ("6", False), ("7", False)]},
        {"question": "What is 6 * 2?", "answers": [("12", True), ("10", False), ("14", False), ("11", False)]},
        {"question": "What is 9 - 3?", "answers": [("6", True), ("5", False), ("7", False), ("4", False)]},
        {"question": "What is 8 / 2?", "answers": [("4", True), ("3", False), ("5", False), ("6", False)]},
        {"question": "What is 4 + 6?", "answers": [("10", True), ("9", False), ("11", False), ("8", False)]},
        {"question": "What is 6 + 1?", "answers": [("7", True), ("6", False), ("8", False), ("9", False)]},
        {"question": "What is 5 - 3?", "answers": [("2", True), ("4", False), ("3", False), ("1", False)]},
    ]

    async with async_session() as session:
        try:
            for q in questions:
                question_obj = Question(question=q["question"])
                session.add(question_obj)
                await session.flush()  # ale trzeba flush jesli chce id miec dostepne od razui. Flush to generate an ID for the question, ale nie potrzebne jeśli autoincrement true w deginicji
                for answer, is_correct in q["answers"]:
                    answer_obj = Answer(answer=answer, ans_validation=is_correct, question_id=question_obj.id)
                    session.add(answer_obj)

            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Błąd podczas dodawania użytkownika: {e}")


async def insert_user(nick: str, plain_password: str) -> User:
    async with async_session() as session:
        try:
            # Czy użytkownik z podanym nickiem już istnieje?
                stmt = select(User).where(User.nick == nick)
                result = await session.execute(stmt)
                existing_user = result.scalars().first()

                # Jeśli istnieje, zwróć komunikat
                if existing_user:
                    print(f"Użytkownik z nickiem '{nick}' już istnieje!")
                    return None

                # Hashowanie hasła
                hashed_password = AccessServices.get_password_hash(plain_password)


                # Tworzenie obiektu użytkownika
                new_user = User(
                    nick=nick,
                    save_password=hashed_password,
                    name='name',
                    surname='surname',
                    email='em@a.il',
                    role='student'

                )

                # Dodanie do sesji i zapis do bazy
                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)  # Pobranie odświeżonego obiektu z bazy

                print(f"Użytkownik '{nick}' został dodany do bazy danych.")
                return new_user  # Zwróć dodanego użytkownika

        except Exception as e:
            # W przypadku błędu wycofaj transakcję
            await session.rollback()
            print(f"Błąd podczas dodawania użytkownika: {e}")
            return None

if __name__ == "__main__":
    asyncio.run(main())

