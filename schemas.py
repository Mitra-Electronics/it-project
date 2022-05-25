from typing import Any, Literal
from pydantic import BaseModel, EmailStr

class AccInfo(BaseModel):
    first_name : str
    last_name : str
    email : EmailStr
    username : str
    country : Literal['India', 'Pakistan', 'Bangladesh', 'Sri Lanka', 'Nepal', 'Bhutan', 'Maldives', 'Afghanisthan', 'Iran', 'United States of America', 'United Kingdom']

class Account(AccInfo):
    password : str
    receive_opt_emails : bool

class Login(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    token: str

class TokenData(BaseModel):
    username: str
    expire: Any

class GameInfo(BaseModel):
    game_name: str
    private_room: bool
    expires_on: str

class Game(GameInfo):
    created_by: str
    created_on: str
    room_code: str
    