from fastapi import FastAPI
from app.quiz.routes import quiz_router
from fastapi.staticfiles import StaticFiles


app = FastAPI()
# Mount folder "static" jako miejsce, z którego serwowana będzie zawartość frontendu

app.mount("/app/static", StaticFiles(directory="app/static"), name="question")

app.include_router(quiz_router)

#to tylko w jednym miejscu i zosytawiam w config
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get('/')#needs log in form
def index():
    #insert click to route @app.get('/start')
    return {'message' : 'Welcome to a test , after you log in there is 30 min to fulfill the test '}
#(30 min topken)

