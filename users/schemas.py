from pydantic import BaseModel, EmailStr, SecretStr
from scripts.regsetup import examples, description

from others import Field


class BaseUser(BaseModel):
    nick: str | None = None
    name: str
    surname: str
    email: EmailStr

class DbUser(BaseUser):
    id: int
    save_password: SecretStr = Field(exclude=True, examples=["examople12pass"], description='type pass, dont forget') # hashed
    ## SecretStr =  przy probie drukowania daje gwiazdki
    # exclude=True - przy próbie serializacji obiektu - do json lub dict to pole nie bedzie included
    role: str = "student"
    disabled : bool = False
    # student / teacher -> teacher does not create account, he gets one created from asministrator, so by the side is omnly possible to create student

    class Config():
        from_attributes = True




class GetUser(BaseUser):
    password: str

class ReturnUser(BaseUser):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
