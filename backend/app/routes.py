from fastapi import FastAPI
from fastapi import APIRouter
from app.quiz.routes import quiz_router


router = APIRouter()


@router.get("/")
def index():
    return {
        "message": "Welcome to a test , after you log in there is 30 min to fulfill the test "
    }


def register_routes(app: FastAPI):
    app.include_router(router, tags=["index"])
    app.include_router(quiz_router, tags=["quiz"])
