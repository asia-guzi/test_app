

from .schemas import GetUser, DbUser, TokenData
from .config import pwd_context, oauth2_scheme, SECRET_KEY, ALGORITHM


from http.client import HTTPException


from datetime import datetime, timedelta, timezone
from typing import Annotated




import jwt
from fastapi import Depends, HTTPException, status

from jwt.exceptions import InvalidTokenError


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

    @staticmethod
    async?
    def save_user(user_in: GetUser):
        hashed_password = AccessServices.get_password_hash(user_in.password)
        user_in_db = DbUser(**user_in.dict(), hashed_password=hashed_password)
        print("User saved! ..not really")
        return user_in_db

    @staticmethod
    async?
    def get_user(db, username: str):
        if username in db:
            user_dict = db[username]
            return DbUser(**user_dict)


    def add_user(self):
        pass

    def get_grades(self):
        pass


class AccessServices:

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

    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        """
        Decode the received token, verify it, and return the current user.

        If the token is invalid, return an HTTP error right away.
        :return:
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        user = UserService.get_user(fake_users_db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    @classmethod
    def authenticate_user(cls, fake_db, username: str, password: str):
        #def fake_decode_token(token):
        """
        And another one to authenticate and return a user.
        :param fake_db:
        :param username:
        :param password:
        :return:
        """

        user = UserService.get_user(fake_db, username)
        if not user:
            return False
        if not cls.verify_password(password, user.hashed_password):
            return False
        return user


    @staticmethod
    async def get_current_active_user(
            current_user: Annotated[User, Depends(get_current_user)],
    ):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
