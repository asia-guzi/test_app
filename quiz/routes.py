
from typing import Annotated
from fastapi import APIRouter, Depends, Response, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
# from users.services import AccessServices
# #from users.config import  oauth2_scheme
from .services import TestService
from .schemas import GetQuestion, UserResponse
from db.dependencies import get_session
from .config import TEST_SIZE
from users.models import User




# quiz_router = APIRouter(
#     dependencies=[Depends(oauth2_scheme)]  # Globalne wymuszanie tokenu
# )

quiz_router = APIRouter(
tags=['quiz']
)

current_user = User(nick='nick',save_password='pass')


@quiz_router.get('/start') #, tags=['quiz'])
async def start_tests( session : Annotated[AsyncSession, Depends(get_session) ]
                      ):
    """     #current_user: Annotated[str, Depends(AccessServices.get_current_active_user)]
       #,token: Annotated[str, Depends(oauth2_scheme)]"""
    #jesli jeszcze nie ma w sloniku - nie mozesz drugiego testu
    print('bt')

    test_set = await TestService.create_test(current_user.nick, session)
    print('at')

    # test_set = await TestService.create_test(current_user, session)
    if len(test_set.questions) < TEST_SIZE: #in case not enough questions in db ect
            # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':'Test not avaiable'}
        # #nie trzeba zwracac response czy cos, starczy ze ustawie jej parametry ale mozna skrcic poprzez exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not avaiable")
    # return RedirectResponse('/question/1')
    return RedirectResponse(f'/frontend/question/{1}')


@quiz_router.get("/frontend/question/{id}", tags=["quiz"])
async def serve_static_question(id: int):
    """
    Przekierowuje użytkownika do dynamicznie zmodyfikowanej strony statycznej
    z przekazaniem parametru `id` w URL.
    """
    url_with_id = f"/static/question.html?id={id}"
    return RedirectResponse(url_with_id)

# would it be better to distinguish on @app.get('/question/{id}') and @app.post('/question/{id}') -decided to distinguish
@quiz_router.get('/question/{id}', response_model=GetQuestion, tags=['quiz']) #, methods=['GET', 'POST'])
async def get_questions(id: int
                 # , current_user: Annotated[str, Depends(AccessServices.get_current_active_user)]
                  # , request: Request
                  # , question : TestQuestion = None
                  # , response: Annotated[UserResponse, Form()] = None
                        ):
    print('odpalone')
    # if request.method == "GET":
    response = await TestService.get_question(user=current_user.nick, id=id)
    print('response : ', response)
    return response

@quiz_router.post('/question/{id}', tags=['quiz']) #, methods=['GET', 'POST'])
#async
def pass_answers(id: int
#, current_user: Annotated[str, Depends(AccessServices.get_current_active_user)]
                # , request: Request
                 , question : UserResponse
                 #, response: Annotated[UserResponse, Form()] = None
        ):
    print(question)
    return TestService.submit_answer(user='nick', id=id, question=question)


@quiz_router.get('/end_test', tags=['quiz']) #is it ok to be get, when i create test outcome in backend|?
async def finish( #current_user: Annotated[str, Depends(AccessServices.get_current_active_user)],
           #tutaj pytanie czy get czy post - bo tworze test w db, ale nic nie wkladam od klienta juz
            #z drugiej strony - wywołanie z submit test wywoływalo sie z post i tu jakj bylo get to byl blad wiec do przemysdalenia
            session : Annotated[AsyncSession, Depends(get_session) ]):
            print('end in')
            ret =  await TestService.submit_test(user=current_user.nick, session=session)
            print('ret', ret)
            return ret
#
# @app.post('/create_q', status_code=status.HTTP_201_CREATED)
# def finish(session : Session = Depends(get_session)):
#     session.add(Question)
#     return {"message": "test finished"}
