
from fastapi import FastAPI
from quiz.routes import quiz_router
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Mount folder "static" jako miejsce, z którego serwowana będzie zawartość frontendu
app.mount("/static", StaticFiles(directory="static"), name="question")

app.include_router(quiz_router)


@app.get('/')#needs log in form
def index():
    #insert click to route @app.get('/start')
    return {'message' : 'Welcome to a test , after you log in there is 30 min to fulfill the test '}
#(30 min topken)





