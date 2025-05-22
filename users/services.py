from __future__ import annotations
#sluzy do tego zeby rozpoznac klasę, gdy chce sie do niej odwołać w jednej z jej metod, bo to oznacz\a ze ta klasa nie jest do konca zdefiniowana i inaczej python doda blad
from .models import User
from .schemas import DbUser #, TokenData, GetUser
from .config import pwd_context, SECRET_KEY, ALGORITHM #, oauth2_scheme
from db.dependencies import get_session
# from sqlalchemy.orm import Session
from sqlalchemy.future import select  # Wymaga SQLAlchemy 1.4+
from sqlalchemy.ext.asyncio import AsyncSession

from http.client import HTTPException


from datetime import datetime, timedelta, timezone
from typing import Annotated





import jwt
from fastapi import Depends, HTTPException #, status
# from jwt.exceptions import InvalidTokenError


#
# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }


class UserService:

    # @classmethod
    # async?
    # def add_user / save_user(cls
    #                           , user_in: GetUser):
    #     hashed_password = AccessServices.get_password_hash(user_in.password)
    #     user_in_db = DbUser(**user_in.dict(), hashed_password=hashed_password)
    #   awaqit cls.get_user(USERBNAME)
    #     db. sprawdz czy juz istnial
    #     dodaj\ .add
    #
    #         .commit
    #     .refresh
    #     .return
    #     .return
    #
    #     print("User saved! ..not really")
    #     return user_in_db

    def get_grades(self):
        pass

    def delete_user(self):
        pass

    def update_user(self):
        pass


class AccessServices:

    @staticmethod
    async def get_user(session: Annotated[AsyncSession, Depends(get_session)]
             ,username: str
                      #, session : AsyncSession = Depends(get_session) #- oba zapisy poprawne ale annotated nowszy i lepszy
                       ):

        result = await session.execute(
            select(User).where(User.nick == username)  #
        )

        user_orm = result.scalars().first()  # Pobierz pierwszy wynik lub None

        # Jeśli znajdziemy użytkownika, konwertujemy go na model Pydantic (DbUser)
        if user_orm:
            return DbUser.model_validate(user_orm)  # Wymaga, aby DbUser miał `orm_mode = True`

        # Jeśli użytkownik nie istnieje, możemy na przykład zwrócić None lub podnieść błąd
        return None  # False

    @staticmethod
    def get_password_hash(password : str) -> str:
        """
        Create a utility function to hash a password coming from the user.
        :return:
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
        And another utility to verify if a received password matches the hash stored.

        :param plain_password:
        :param hashed_password:
        :return:
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        """
        Create a utility function to generate a new access token.

        :param data:
        :param expires_delta:
        :return:
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @classmethod
    async def get_current_user(cls
                               ,session: Annotated[AsyncSession, Depends(get_session)]):

        user = await cls.get_user(username='nick', session=session)
        return user
    # @classmethod
    # async def get_current_user( cls,
    #      token: Annotated[str, Depends(oauth2_scheme)]):
    #     """
    #     Decode the received token, verify it, and return the current user.
    #
    #     If the token is invalid, return an HTTP error right away.
    #     :return:
    #     """
    #     credentials_exception = HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Could not validate credentials",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    #     try:
    #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #         username = payload.get("sub")
    #         if username is None:
    #             raise credentials_exception
    #         token_data = TokenData(username=username)
    #     except InvalidTokenError:
    #         raise credentials_exception
    #     user = await cls.get_user(username=token_data.username)
    #     if user is None:
    #         raise credentials_exception
    #     return user

    @classmethod
    async def authenticate_user(cls
                                , session : [AsyncSession, Depends(get_session)]
                                , username: str, password: str):
        #def fake_decode_token(token):
        """
        And another one to authenticate and return a user.
        """

        user = await cls.get_user(username=username, session=session)
        if not user:
            return False
        if not cls.verify_password(password, user.hashed_password):
            return False
        return user


    @staticmethod
    async def get_current_active_user(

           current_user: Annotated[User, Depends(AccessServices.get_current_user)]

    ):
        # current_user =  cls.get_current_user()
        # Depends("AccessServices.get_current_user")
        """
          Ten problem można łatwo naprawić, używając odroczonej rozpoznawalności typów.

          Rozwiązanie z opóźnionym rozpoznawaniem typów adnotacji
          Możesz to naprawić, używając łańcuchowej nazwy klasy (string) w Depends dla AccessServices.get_current_user. FastAPI i Python poradzą sobie z poprawną interpretacją tych typów w runtime.
        """
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
