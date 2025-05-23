

from fastapi import FastAPI

# from sqlalchemy.sql.annotation import Annotated,

# from sqlalchemy import func
# from sqlalchemy.orm import joinedload, Session
# from users.users import Question, Answer
# from db.dependencies import get_session
from quiz.routes import quiz_router





"""

Jeśli używasz SQLAlchemy do zarządzania bazą danych i FastAPI jako frameworka backendowego, nie musisz samodzielnie uruchamiać pętli event loop (asyncio.run()), ponieważ FastAPI ma wbudowaną pętlę event loop, która jest automatycznie zarządzana. Framework FastAPI samodzielnie obsługuje event loop, a także integruje się z asynchronicznymi funkcjami i bibliotekami.

Poniżej znajdziesz wyjaśnienie najlepszych praktyk dla FastAPI i SQLAlchemy, co zrobić w kontekście zarządzania pętlą event loop.

Czy muszę martwić się o asyncio.run() w FastAPI?
Nie, w FastAPI nie musisz explicitnie wywoływać asyncio.run(), ponieważ:

FastAPI automatycznie korzysta z pętli event loop.
FastAPI dba o wszystkie aspekty zarządzania pętlą i asynchronicznymi funkcjami.
Gdy tworzysz aplikację FastAPI i definiujesz funkcje asynchroniczne (async def), FastAPI automatycznie czeka (await) na ich wykonanie w swojej pętli event loop.

Jak działa SQLAlchemy z FastAPI i event loop?
Asynchroniczny SQLAlchemy:
Jeśli używasz SQLAlchemy w trybie async (np. create_async_engine i AsyncSession), to:

Musisz upewnić się, że wszystkie interakcje z bazą są obsługiwane w funkcjach asynchronicznych (async def).
FastAPI uruchomi te funkcje w ramach swojej pętli event loop.
Przykład połączenia FastAPI z SQLAlchemy (asynchronicznie):
python


from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Konfiguracja bazy danych
DATABASE_URL = "sqlite+aiosqlite:///test.db"  # Przykład SQLite
Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_="AsyncSession")

# Tworzenie bazy danych
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Dependency do sesji SQLAlchemy
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# FastAPI app
app = FastAPI()

# Endpoint dodający dane do bazy danych
@app.post("/add-user/")
async def add_user(nick: str, db: AsyncSession = Depends(get_db)):
    from models import User  # Model SQLAlchemy
    new_user = User(nick=nick, save_password="hashed_password")
    db.add(new_user)
    await db.commit()
    return {"success": True}
Jak działa pętla event loop w FastAPI?
Gdy użytkownik wywołuje endpoint API np. /add-user/, FastAPI automatycznie uruchamia Twoją funkcję asynchroniczną w swojej pętli event loop.
Twoje funkcje asynchroniczne (np. add_user) mogą używać await dla funkcji SQLAlchemy albo innych bibliotek.
FastAPI dba o to, żeby wszystko działało w trybie asynchronicznym.
Możesz więc skupić się tylko na pisaniu funkcji asynchronicznych (async def) i nie musisz zarządzać pętlą event loop samodzielnie.

Jeśli potrzebujesz asynchronicznej inicjalizacji w FastAPI
Czasami musisz zrobić jakieś akcje inicjalizujące (np. utworzyć tabele w bazie danych przed startem aplikacji). Można to zrobić przed startem serwera FastAPI, unikając ręcznego zarządzania pętlą.

FastAPI oferuje zdarzenie on_startup, które pozwala na wykonanie kodu (w tym asynchronicznego) podczas startu aplikacji.

Przykład inicjalizacji tabel w FastAPI:
python


from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy setup
DATABASE_URL = "sqlite+aiosqlite:///test.db"
Base = declarative_base()
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Tworzenie bazy danych (asynchronicznie) podczas startu aplikacji
async def create_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# FastAPI app
app = FastAPI(on_startup=[create_db]) 
"""
app = FastAPI()
from fastapi.staticfiles import StaticFiles
# Mount folder "static" jako miejsce, z którego serwowana będzie zawartość frontendu

app.mount("/static", StaticFiles(directory="static"), name="question")

app.include_router(quiz_router)

#to tylko w jednym miejscu i zosytawiam w config
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get('/')#needs log in form
def index():
    #insert click to route @app.get('/start')
    return {'message' : 'Welcome to a test , after you log in there is 30 min to fulfill the test '}
#(30 min topken)





