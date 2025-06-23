import os
from fastapi import FastAPI
from app.quiz.routes import quiz_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # adres twojego frontendu
    allow_credentials=True,
    allow_methods=["*"],  # dozwolone metody HTTP (GET, POST, itp)
    allow_headers=["*"],  # dozwolone nagłówki HTTP
    expose_headers=["Location"],  # <-- to jest kluczowe!

)


# Mount folder "static" jako miejsce, z którego serwowana będzie zawartość frontendu

# # app.mount("/app/static", StaticFiles(directory="./static"), name="question") #works from here, does not work from tests
# static_dir = os.path.join(os.path.dirname(__file__), "static")
# app.mount("/app/static", StaticFiles(directory=static_dir), name="static")

app.include_router(quiz_router)

# to tylko w jednym miejscu i zosytawiam w config
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")  # needs log in form
def index():
    # insert click to route @app.get('/start')
    return {
        "message": "Welcome to a test , after you log in there is 30 min to fulfill the test "
    }


# (30 min token)
