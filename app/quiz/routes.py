
#test is avaialble only gor lohed in users, tgherefore the dependency get_current_active_user
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

#from users.config import  oauth2_scheme
from .services import TestService
from .schemas import GetQuestion, UserResponse
from app.db.dependencies import get_session
from .config import TEST_SIZE
from app.users.models import User

# quiz_router = APIRouter(
#     dependencies=[Depends(oauth2_scheme)]  # Globalne wymuszanie tokenu
# )

quiz_router = APIRouter(
tags=['quiz'] #nie trzeba w kazdym z osobna, tylko mozna w routerze ustawic tags
)

current_user = User(nick='nick',save_password='pass')

@quiz_router.get('/start') #, tags=['quiz'])
async def start_tests( session : Annotated[AsyncSession, Depends(get_session) ]
        #current_user: Annotated[str, Depends(AccessServices.get_current_active_user)]
        #, response: Response
        #,token: Annotated[str, Depends(oauth2_scheme)]
                      ) -> RedirectResponse:
    """
    fetch random questions from the database, and initiate test for user

    :param session: AsyncSession - database session
    :return: RedirectResponse - rout to the for the first question
    """

    #jesli jeszcze nie ma w sloniku - nie mozesz drugiego testu
    # return current test

    test_set = await TestService.create_test(current_user.nick, session)

    if len(test_set.questions) < TEST_SIZE: #in case not enough questions in db ect
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not avaiable")

    # return RedirectResponse(f'/question/{1}')
    return RedirectResponse(f'/frontend/question/{1}')


@quiz_router.get("/frontend/question/{id}", tags=["quiz"])
async def serve_static_question(id: int) -> RedirectResponse:
    """
    fetch random questions from the database, and initiate test for user

    :param id: int - id passed as part of URL
    :return: RedirectResponse - rout to the for the current front
    """

    url_with_id = f"/static/question.html?id={id}"
    return RedirectResponse(url_with_id)


@quiz_router.get('/question/{id}', response_model=GetQuestion, tags=['quiz']) #, methods=['GET', 'POST'])
async def get_questions(id: int
                 # , current_user: Annotated[str, Depends(AccessServices.get_current_active_user)]
                  # , request: Request
                  # , question : TestQuestion = None
                  # , response: Annotated[UserResponse, Form()] = None
                        ):
    """

    """
    response = await TestService.get_question(user=current_user.nick, id=id)
    return response

@quiz_router.post('/question/{id}', tags=['quiz']) #, methods=['GET', 'POST'])
#async
def pass_answers(id: int
#, current_user: Annotated[str, Depends(AccessServices.get_current_active_user)]
                # , request: Request
                 , question : UserResponse
                 #, response: Annotated[UserResponse, Form()] = None
        ):
    return TestService.submit_answer(user='nick', id=id, question=question)


# should be get or post, if finally it creates test result in db
@quiz_router.get('/end_test', tags=['quiz']) #is it ok to be get, when i create test outcome in backend|?
async def finish( #current_user: Annotated[str, Depends(AccessServices.get_current_active_user)],
            session : Annotated[AsyncSession, Depends(get_session) ]):


            ret =  await TestService.submit_test(user=current_user.nick, session=session)
            return ret


# @app.post('/create_q', status_code=status.HTTP_201_CREATED)
# def finish(session : Session = Depends(get_session)):
#     session.add(Question)
#     return {"message": "test finished"}
