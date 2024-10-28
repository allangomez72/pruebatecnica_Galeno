from typing import Annotated

from fastapi import APIRouter, Depends
from schema.user_schema import UserSchema
from config.db import conn
from model.user import user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
user = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@user.get('/')
def root():
    return {"message": "Hello World"}

@user.post('/api/user')
def create_user(data_user:UserSchema):
    print(data_user)

@user.post('/token')
def logi(from_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    return from_data