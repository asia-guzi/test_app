

from fastapi import FastAPI, Request, status, HTTPException, Form
from fastapi.responses import RedirectResponse, Response
# from sqlalchemy.sql.annotation import Annotated
from typing import Annotated
from tests.schema import UserResponse, TestQuestion
# from sqlalchemy import func
# from sqlalchemy.orm import joinedload, Session
# from users.users import Question, Answer
# from db.dependencies import get_session


app = FastAPI()

test_size = 3 #20 z user session, albo z model test - coś takiego

questions_sample = {
    1: {
        "question": "2+1",
        "choices": [("5",False ), ("4", False), ("8",False ), ("3",True )]
    },
    2: {
        "question": "2+2",
        "choices": [("5",False ), ("4", True), ("8",False ), ("3",False )]
    },
    3: {
        "question": "2+3",
        "choices": [("5",True ), ("4", False), ("8",False ), ("3",False )]
    }
}

question = questions_sample[1]
print(question)

@app.get('/')
def index():
    #insert click to route @app.get('/start')
    return {'message' : 'Welcome to a test'}


# async def get_questions():
#
#     return await ( #zamienic na execute query i doda
#         session.query(Question)
#         .options(joinedload(Question.answers))  #need a complet of Q + A
#         .order_by(func.random()) #select questions from base at random
#         .limit(test_size)
#         .all()
#     )

@app.get('/start')
#async
def start_tests(response: Response):

    test_set = questions_sample #await get_questions()
    if len(test_set) < test_size:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':'Test not avaiable'}
        # #nie trzeba zwracac response czy cos, starczy ze ustawie jej parametry ale mozna skrcic poprzez exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not avaiable")
    return RedirectResponse('/question/1')



    # for question in test_set:
    #
    #
    #     print(f"Pytanie: {question.title}")
    #     for answer in question.answers:  # Wszystko już jest w pamięci
    #         print(f"- Odpowiedź: {answer.content}")
    #         `
    #
    # # questions = await questions
    # return test_set #questions


# would it be better to distinguish on @app.get('/question/{id}') and @app.post('/question/{id}')
@app.api_route('/question/{id}', methods=['GET', 'POST'])
#async
def pass_answers(id: int, request: Request, question : TestQuestion = None, response: Annotated[UserResponse, Form()] = None):

    if request.method == "GET":
        question = questions_sample[id]
        print(question)
        if id <= test_size:
            return question
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND)



    if request.method == "POST":

        print(response)

        if id < test_size:
            return RedirectResponse(f'/question/{id+1}')
        elif id == test_size :
            return RedirectResponse('/end_test')
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get('/end_test')
def finish():
    return {"message": "test finished"}

#
# @app.post('/create_q', status_code=status.HTTP_201_CREATED)
# def finish(session : Session = Depends(get_session)):
#     session.add(Question)
#     return {"message": "test finished"}