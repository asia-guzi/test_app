@validate_call
Dzięki @validate_call, możesz automatycznie upewnić się, że wszystkie argumenty przekazane do funkcji:

Spełniają określone typy danych (zgodnie z adnotacjami typów w funkcji).
Są poprawne według reguł walidacji wbudowanych w Pydantic.
Zostają automatycznie przekonwertowane na wymagane typy (jeśli to możliwe, np. str → bytes, int → float).

The validate_call() decorator allows the arguments passed to a function to be parsed and validated using the function's annotations before the function is called.

While under the hood this uses the same approach of model creation and initialisation (see Validators for more details), it provides an extremely easy way to apply validation to your code with minimal boilerplate.

Example of usage:


from pydantic import ValidationError, validate_call


@validate_call
def repeat(s: str, count: int, *, separator: bytes = b'') -> bytes:
    b = s.encode()
    return separator.join(b for _ in range(count))

@validate_call
def how_many(num: Annotated[int, Field(gt=10, alias='number')]):
    return num

from pydantic import validate_call


@validate_call
def repeat(s: str, count: int, *, separator: bytes = b'') -> bytes:
    b = s.encode()
    return separator.join(b for _ in range(count))


a = repeat('hello', 3)
print(a)
#> b'hellohellohello'

b = repeat.raw_function('good bye', 2, separator=b', ')
print(b)
#> b'good bye, good bye'



------------------------------------------------------

id: int | None = Field(default=None, primary_key=True)
id to pole w modelu. Reprezentuje kolumnę tabeli z kluczem głównym (primary key).
Typ:
int | None oznacza, że id może być int (liczbą całkowitą) albo None (puste/niezainicjalizowane).
Jest to alternatywny zapis dla Optional[int] (sprowadzony z typing) w Pythonie 3.10 i wyżej.
Field:
To konstruktor SQLModel dla pól tabeli, który pozwala dodać szczegóły i konfigurację kolumny w bazie danych, np.:
default=None: Wartość domyślna kolumny to None.
primary_key=True: Pole to jest kluczem głównym tabeli.



------------------------------------------------------------

# Code above omitted 👆

class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str


class HeroPublic(HeroBase):
    id: int


class HeroCreate(HeroBase):
    secret_name: str


class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None

# Code below omitted 👇
    @
    async def create_hero(hero: Hero, session: SessionDep) -> Hero:
        '''https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-hero'''
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero

    # Code above omitted 👆

    @app.get("/heroes/")
    def read_heroes(
            session: SessionDep,
            offset: int = 0,
            limit: Annotated[int, Query(le=100)] = 100,
    ) -> list[Hero]:
        heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
        return heroes

    # Code above omitted 👆

    @app.delete("/heroes/{hero_id}")
    def delete_hero(hero_id: int, session: SessionDep):
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        session.delete(hero)
        session.commit()
        return {"ok": True}
@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

# Code above omitted 👆

@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

# Code below omitted 👇

# Code above omitted 👆

@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db

# Code below omitted 👇


------------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict



--------------------------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

??????????????????????????????????????????????

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


Request body + path + query parameters¶
You can also declare body, path and query parameters, all at the same time.

FastAPI will recognize each of them and take the data from the correct place.


Python 3.10+

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

The function parameters will be recognized as follows:

If the parameter is also declared in the path, it will be used as a path parameter.
If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.

----------------------------------------------------------------------------------
Additional validation¶
We are going to enforce that even though q is optional, whenever it is provided, its length doesn't exceed 50 characters.

Import Query and Annotated¶
To achieve that, first import:

Query from fastapi
Annotated from typing

Python 3.10+

from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


--------------------------------------------------------
from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items

-----------------------------------------------------------------

from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items

---------------------------------------------------------------------------------
from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

--------------------------------------------------------------------------------

import random
from typing import Annotated

from fastapi import FastAPI
from pydantic import AfterValidator

app = FastAPI()

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


@app.get("/items/")
async def read_items(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}













-------------------------------------------------

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user


-----------------------------

from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type: str = "car"


class PlaneItem(BaseItem):
    type: str = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]

----------------------------

from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

------------------

from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


CommonsDep = Annotated[dict, Depends(common_parameters)]


@app.get("/items/")
async def read_items(commons: CommonsDep):
    return commons


@app.get("/users/")
async def read_users(commons: CommonsDep):
    return commons

--------------------------------------------
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


---------------------