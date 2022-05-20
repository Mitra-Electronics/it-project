from pymongo import MongoClient

from schemas import Account, Login
from auth_func import hash_password, verify_password
from config import MONGO_DB_URL

db_connect = MongoClient(MONGO_DB_URL)

collection = db_connect.get_database("discord")

acc = collection.accounts

def acc_insert(data: Account):
    email_find = acc_find_email(data.email)
    username_find = acc_find_username(data.username)
    if email_find == False and username_find == False:
        acc.insert_one({'first_name':data.first_name,
                        'last_name':data.last_name,
                        'email':data.email,
                        'username':data.username,
                        'hashed_password':hash_password(data.password),
                        'receive_opt_emails':data.receive_opt_emails})

        return "Your account has been created sucessfully."
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
    if account != []:
        if not verify_password(data.password, account['hashed_password']):
            return ["Wrong password", account]
        else:
            return ["Logged in", account]
    else:
        return ["There is no account registered with this email", account]

def acc_find_username(username: str):
    if acc.find_one({"username":username}) == None:
        return False
    else:
        return True
    
