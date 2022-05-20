import secrets

from passlib.context import CryptContext

from config import DEPRECIATED, SCHEMES, SECRET_KEY

pwd_context = CryptContext(schemes=SCHEMES, deprecated=DEPRECIATED)

def hash_password(password: str):
    return pwd_context.hash(SECRET_KEY+password+"132")

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(SECRET_KEY+password+"132", hashed_password)
    