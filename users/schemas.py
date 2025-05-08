from pydantic import BaseModel, EmailStr

class BaseUser(BaseModel):

    nick : str
    - password =
    name : str
    surname : str
    role : str  # student / teacher
    email = EmailStr


class DbUser(BaseModel):
    id =


