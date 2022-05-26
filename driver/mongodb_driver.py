import secrets
from datetime import datetime

from pymongo import MongoClient

from auth_func import hash_password, verify_password
from config import MONGO_DB_URL
from schemas import Account, GameInfo, Login

db_connect = MongoClient(MONGO_DB_URL)

collection = db_connect.get_database("discord")

acc = collection.accounts
game_db = collection.games

def acc_insert(data: Account):
    email_find = acc_find_email(data.email)
    username_find = acc_find_username(data.username)
    if email_find == False and username_find == False:
        acc.insert_one({'first_name':data.first_name,
                        'last_name':data.last_name,
                        'email':data.email,
                        'username':data.username,
                        'country':data.country,
                        'hashed_password':hash_password(data.password),
                        'created_on':datetime.utcnow(),
                        'receive_opt_emails':data.receive_opt_emails})

        return True
    elif email_find == True and username_find == False:
        return "An account has been already registered with this email. Please try with another email."
    else:
        return "An account has been already registered with the same email and username. Please try with another email and username."

def get_acc_username(username: str):
    return acc.find_one({"username":username})

def get_acc(email: str):
    return acc.find_one({"email":email})

def acc_find_email(email: str):
    if get_acc(email) == None:
        return False
    else:
        return True

def acc_login(data: Login):
    account = get_acc(data.email)
    if account != None:
        if not verify_password(data.password, account['hashed_password']):
            return ["Wrong password", "0"]
        else:
            return ["Logged in", account]
    return ["There is no account registered with this email", "0"]

def acc_delete(user: Account):
    deleted = acc.delete_one({"email":user.email, "username":user.username})
    return deleted.deleted_count

def acc_find_username(username: str):
    if acc.find_one({"username":username}) == None:
        return False
    else:
        return True

def room_get(room_code):
    return game_db.find_one({"room_code":room_code})

def gen_tokn():
    arr = ['a', 'b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    tokn: str = ""
    def part():
        tokn = ""
        for i in range(4):
            tokn += secrets.choice(arr)
        return tokn
    tokn = part() + "-" + part() + "-" + part()
    if room_get(tokn) is None:
        return tokn
    else:
        gen_tokn()

def room_create(user: dict, game_det: GameInfo):
    room_code =  gen_tokn()
    try:
        game_db.insert_one({
            "game_name": game_det.game_name,
            "created_by":user["username"],
            "created_on":datetime.utcnow(),
            "private_room": game_det.private_room,
            "room_code":room_code,
            "expires_on": game_det.expires_on,
        })
        return room_code
    except Exception:
        return False
    
