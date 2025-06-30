from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

# from users.config import  oauth2_scheme
from .services import TestService
from .schemas import GetQuestion, UserResponse
from app.db.dependencies import get_session
from .config import TEST_SIZE
from app.users.models import User


quiz_router = APIRouter(
    # tags=["quiz"]
)

current_user = User(nick="nick", save_password="pass")


@quiz_router.get("/start")
async def start_tests(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> JSONResponse:
    """
    fetch random questions from the database, and initiate test for user

    :param session: AsyncSession - database session
    :return: RedirectResponse - rout to the for the first question
    """

    test_set = await TestService.create_test(current_user.nick, session)

    if len(test_set.questions) < TEST_SIZE:  # in case not enough questions in db ect
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Test not avaiable"
        )

    return JSONResponse({"next_question_id": 1})


@quiz_router.get(
    "/question/{id}", response_model=GetQuestion, tags=["quiz"]
)  # , methods=['GET', 'POST'])
async def get_questions(id: int):
    """ """
    response = await TestService.get_question(user=current_user.nick, id=id)
    return response


@quiz_router.post("/question/{id}", tags=["quiz"])
def pass_answers(
    id: int,
    question: UserResponse,
):
    return TestService.submit_answer(user="nick", id=id, question=question)


# should be get or post, if finally it creates test result in db
@quiz_router.get("/end_test", tags=["quiz"])
async def finish(
    session: Annotated[AsyncSession, Depends(get_session)],
):

    ret = await TestService.submit_test(user=current_user.nick, session=session)
    return ret
