from fastapi import FastAPI, HTTPException

from driver.jwt_driver import create_access_token, decode_access_token
from driver.mongodb_driver import (acc_delete, acc_insert, acc_login)
from schemas import AccInfo, Account, Login, Token
from router.game_router import router

app = FastAPI()
app.include_router(router)

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
