from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, EmailStr

class AccInfo(BaseModel):
    first_name : str
    last_name : str
    email : EmailStr
    username : str
    country : Literal['india', 'pakistan', 'bangladesh', 'sri lanka', 'nepal', 'bhutan', 'maldives', 'afghanisthan', 'iran', 'united states of america', 'united kingdom']

    def get_full_name(self):
        return self.first_name + " " + self.last_name

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
    created_on: datetime
    room_code: str

    def get_dict(self):
        return {"name":self.game_name,
            "private_room":self.private_room, 
            "expires_on":str(self.expires_on), 
            "created_by":self.created_by, 
            "created_on":str(self.created_on), 
            "room_code":self.room_code}
    