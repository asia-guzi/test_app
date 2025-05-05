from pydantic import BaseModel

class BaseUser(BaseModel):

    nick : str
    - password =
    name : str
    surname : str
    role : str  # student / teacher


class DbUser(BaseModel):
    id =


