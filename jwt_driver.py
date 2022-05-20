from datetime import datetime, timedelta
from typing import Union

from jose import JWTError, jwt

from config import (ALGORITHM, CREDENTIALS_EXCEPTION,
                    SECRET_KEY)
from schemas import TokenData
from mongodb_driver import get_acc_username


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(username=payload.get("sub"), expire=payload.get("exp"))
        if token_data.username is None:
            raise CREDENTIALS_EXCEPTION
        user = get_acc_username(token_data.username)
        if user is None:
            raise CREDENTIALS_EXCEPTION
        return user
    except JWTError:
        raise CREDENTIALS_EXCEPTION
