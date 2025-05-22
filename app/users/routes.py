#
# from .schemas import ReturnUser, GetUser
#
#
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# import jwt
# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jwt.exceptions import InvalidTokenError
# from passlib.context import CryptContext
# from pydantic import BaseModel
# from fastapi import Depends, HTTPException, Security, status
# from fastapi.security import (
# OAuth2PasswordBearer,
# OAuth2PasswordRequestForm,
# SecurityScopes,
# )
# from datetime import timedelta
# from .schemas import Token
# from main import app
# from .services import AccessServices as ac
# from .config import ACCESS_TOKEN_EXPIRE_MINUTES
#
# from passlib.context import CryptContext
# from pydantic import BaseModel, ValidationError
#
# from typing import Annotated
# # @app.post("/user/", response_model=ReturnUser, status_code=status.HTTP_201_CREATED
# #     , current_user: Annotated[User, Depends(UserService.get_current_user)])
# # async def create_user(user_in: GetUser):
# #     # jeżeli
# #     # już
# #     # istnieje -
# #     #     raise HTTPException(status., detail="The user already exists")
# #     #
# #     #
# #     # user_saved = fake_save_user(user_in)
# #     # return user_saved
# #     pass
#
# # @app.delete("/user/", response_model=ReturnUser, status_code=status.HTTP_201_CREATED)
# # async def delete_user(current_user: Annotated[User, Depends(UserService.get_current_user)]
# #                       , user_in: GetUser):
# #     pass
#
# # @app.put("/user/", response_model=ReturnUser)
# # async def update_user(user_in: GetUser):
# #     #     user_saved = fake_save_user(user_in)
# #     # return user_saved
# #     pass
#
# #------------------------
# @app.post("/token")
# async def login_for_access_token(
# form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
# ) -> Token:
#     """
#     Create a timedelta with the expiration time of the token.
#
#     Create a real JWT access token and return it.
#     :return:
#     """
#     user = ac.authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Incorrect username or password",
#         headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = ac.create_access_token(
#     data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token, token_type="bearer")
#
# # @app.post("/token") - bez perawdziwego tokena
# # async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
# #
# #     user_dict = fake_users_db.get(form_data.username)
# #     if not user_dict:
# #         raise HTTPException(status_code=400, detail="Incorrect username or password")
# #     user = UserInDB(**user_dict)
# #     hashed_password = fake_hash_password(form_data.password)
# #     if not hashed_password == user.hashed_password:
# #         raise HTTPException(status_code=400, detail="Incorrect username or password")
# #
# #     return {"access_token": user.username, "token_type": "bearer"}
# #
#
#
# # @app.get("/users/me/", response_model=User)
# # async def read_users_me(
# #     current_user: Annotated[User, Depends(get_current_active_user)],
# #     ):
# #     return current_user
# #
# #
# #
# # @app.get("/users/me/items/")
# # async def read_own_items(
# #     current_user: Annotated[User, Depends(get_current_active_user)],
# #     ):
# #     return [{"item_id": "Foo", "owner": current_user.username}]
#
#
#
#
#
#
