from tests.models import *
from db.config import async_engine, async_session


def main():
    create_db()
    insert_data()

async def create_db():
    """
    to create tables
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Insert questions and answers
def insert_data():
    session = async_session()

    try:
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


        for q in questions:
            question_obj = Question(question=q["question"])
            session.add(question_obj)
            session.flush()  # Flush to generate an ID for the question
            for answer, is_correct in q["answers"]:
                answer_obj = Answer(answer=answer, ans_validation=is_correct, question_id=question_obj.id)
                session.add(answer_obj)

        session.commit()

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()


# if __name__ == "__main__":
#     main()

