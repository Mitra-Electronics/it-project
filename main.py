from fastapi import FastAPI
from mongodb_driver import acc_insert, acc_login
from jwt_driver import create_access_token, decode_access_token

from schemas import Account, Login, Token, AccInfo

app = FastAPI()

@app.post('/signup')
def signup(data: Account):
    message = acc_insert(data)
    return {"data":message}

@app.post('/login')
def login(data: Login):
    msg = acc_login(data)
    if msg[0] == 'Logged in':
        return {'data':msg[0], 'logged_in':True, "access_token":create_access_token({"sub":msg[1]["username"]})}
    else:
        {"data":msg[0], 'logged_in':False}

@app.post('/get/account')
def get_acc_info(token: Token):
    user = decode_access_token(token.token)
    return AccInfo(**user)
