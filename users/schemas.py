from pydantic import BaseModel, EmailStr
from sqlalchemy import Boolean


class BaseUser(BaseModel):
    nick: str | None = None
    name: str
    surname: str
    email: EmailStr

class DbUser(BaseUser):
    id: int
    save_password: str  # hashed
    role: str = "student"
    disabled : Boolean = False
    # student / teacher -> teacher does not create account, he gets one created from asministrator, so by the side is omnly possible to create student

class GetUser(BaseUser):
    password: str

class ReturnUser(BaseUser):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
