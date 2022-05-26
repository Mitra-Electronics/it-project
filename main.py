from fastapi import FastAPI, HTTPException

from driver.jwt_driver import create_access_token, decode_access_token
from driver.mongodb_driver import (acc_delete, acc_insert, acc_login, room_create,
                            room_get)
from schemas import AccInfo, Account, GameInfo, Login, Token

app = FastAPI()

@app.post("/signup")
def signup(data: Account):
    message = acc_insert(data)
    if message == True:
        return {"status":"ok",'registered':True}
    else:
        return {"status":"not ok","data":message, 'registered':False}

@app.post("/login")
def login(data: Login):
    msg = acc_login(data)
    if msg[0] == "Logged in":
        return {"status":"ok",'data':msg[0], "logged_in":True, "access_token":create_access_token({"sub":msg[1]['username']})}
    else:
        return {"status":"not ok","data":msg[0], "logged_in":False}

@app.post("/get/account")
def get_acc_info(token: Token):
    return {"status":"ok", "data":AccInfo(**decode_access_token(token.token))}

@app.post("/delete/account")
def delete_account(token: Token):
    del_func = acc_delete(AccInfo(**decode_access_token(token.token)))
    if del_func < 1:
        raise HTTPException(
            status_code=204,
            detail="Account doesn't exist",
        )
    else:
        return {"status":"ok","data":"deleted", "deleted":True}

@app.post("/game/verify/{room_code}")
async def verify_game(token: Token, room_code: str):
    decode_access_token(token.token)
    room = room_get(room_code)
    if room is None:
        return {"status":"not ok", "data":"room not found", "room_found":False}
    else:
        return {"status":"not ok", "data":"room not found", "room_found":False}

@app.post("/game/create")
def create_game(auth_token: Token, room: GameInfo):
    code = room_create(decode_access_token(auth_token.token), room)
    if code is False:
        return {"status":"not ok", "room_created":False}
    return {"status":"ok", "room_created":True, "room_code":code}

@app.websocket("/game/join/{room_code}")
async def handler(room_code: str):
    room = await room_get(room_code)
    if room is None:
        raise HTTPException(
            status_code=1007,
            detail="Room doesn't exist"
        )
    else:
        pass
