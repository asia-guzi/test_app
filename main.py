

from fastapi import FastAPI, Request, status, HTTPException, Form, Depends
from fastapi.responses import RedirectResponse, Response
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.dependencies import get_session

# from sqlalchemy.sql.annotation import Annotated,
from typing import Annotated
from quiz.schemas import UserResponse, TestQuestion
from fastapi.security import OAuth2PasswordBearer
from quiz.services import TestSet

# from sqlalchemy import func
# from sqlalchemy.orm import joinedload, Session
# from users.users import Question, Answer
# from db.dependencies import get_session


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get('/')
def index():
    #insert click to route @app.get('/start')
    return {'message' : 'Welcome to a test'}




@app.get('/start')
async def start_tests(response: Response
                      ,token: Annotated[str, Depends(oauth2_scheme)]
                      ,session : Session = Depends(get_session)):
       # return {"token": token}
    test_set = await TestSet.get_test()
    if len(test_set) < test_set.size:
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
        question = questions_sample[id-1]
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