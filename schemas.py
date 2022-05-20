from typing import Any
from pydantic import BaseModel, EmailStr

class Account(BaseModel):
    first_name : str
    last_name : str
    email : EmailStr
    username : str
    password : str
    receive_opt_emails : bool

class AccInfo(BaseModel):
    first_name : str
    last_name : str
    email : EmailStr
    username : str

class Login(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    token: str

class TokenData(BaseModel):
    username: str
    expire: Any
    