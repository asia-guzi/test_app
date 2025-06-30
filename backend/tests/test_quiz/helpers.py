import random
from app.quiz.schemas import AnsweredQuestion, DbQuestion, DbAnswer, UserResponse

QUESTION_DATA = [
    {
        "id": 1,
        "question": "Question 1",
        "answers": [
            {"id": 1, "answer": "Answer 1", "question_id": 1, "ans_validation": True},
            {"id": 2, "answer": "Answer 2", "question_id": 1, "ans_validation": False},
            {"id": 3, "answer": "Answer 3", "question_id": 1, "ans_validation": False},
            {"id": 4, "answer": "Answer 4", "question_id": 1, "ans_validation": False},
        ],
    },
    {
        "id": 2,
        "question": "Question 2",
        "answers": [
            {"id": 5, "answer": "Answer 1", "question_id": 2, "ans_validation": False},
            {"id": 6, "answer": "Answer 2", "question_id": 2, "ans_validation": True},
            {"id": 7, "answer": "Answer 3", "question_id": 2, "ans_validation": False},
            {"id": 8, "answer": "Answer 4", "question_id": 2, "ans_validation": False},
        ],
    },
    {
        "id": 3,
        "question": "Question 3",
        "answers": [
            {"id": 9, "answer": "Answer 1", "question_id": 3, "ans_validation": False},
            {"id": 10, "answer": "Answer 2", "question_id": 3, "ans_validation": False},
            {"id": 11, "answer": "Answer 3", "question_id": 3, "ans_validation": True},
            {"id": 12, "answer": "Answer 4", "question_id": 3, "ans_validation": False},
        ],
    },
    {
        "id": 4,
        "question": "Question 4",
        "answers": [
            {"id": 13, "answer": "Answer 1", "question_id": 4, "ans_validation": False},
            {"id": 14, "answer": "Answer 2", "question_id": 4, "ans_validation": False},
            {"id": 15, "answer": "Answer 3", "question_id": 4, "ans_validation": False},
            {"id": 16, "answer": "Answer 4", "question_id": 4, "ans_validation": True},
        ],
    },
    {
        "id": 5,
        "question": "Question 5",
        "answers": [
            {"id": 17, "answer": "Answer 1", "question_id": 5, "ans_validation": False},
            {"id": 18, "answer": "Answer 2", "question_id": 5, "ans_validation": True},
            {"id": 19, "answer": "Answer 3", "question_id": 5, "ans_validation": False},
            {"id": 20, "answer": "Answer 4", "question_id": 5, "ans_validation": False},
        ],
    },
]


def get_AnsweredQuestion_schema(data):
    return AnsweredQuestion(
        question=DbQuestion.model_validate(
            {"id": data["id"], "question": data["question"]}
        ),
        answers=random.sample(
            [DbAnswer.model_validate(answer) for answer in data["answers"]],
            len(data["answers"]),
        ),
    )


def mock_user_responses_collection():
    """
    generator of set of user's collections for each question in test set
    """

    for question in QUESTION_DATA:
        collection = {}
        question_id = question["id"]

        # for question in data_for_tests:
        #     if question['id'] == question_id:

        for answer in question["answers"]:
            if answer["ans_validation"] == True:
                collection["true_response"] = UserResponse(
                    chosen_question_id=question_id, chosen_answer_id=answer["id"]
                )

            elif "false_response" not in collection:
                collection["false_response"] = UserResponse(
                    chosen_question_id=question_id, chosen_answer_id=answer["id"]
                )

        collection["nonexistent_response"] = UserResponse(
            chosen_question_id=question_id, chosen_answer_id=-1
        )
        # break
        yield question, collection
