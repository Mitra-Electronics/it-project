from fastapi.exceptions import HTTPException
from fastapi import status

MONGO_DB_URL = "mongodb://localhost:27017"
#MONGO_DB_URL = "mongodb+srv://main2:fKYgy2PJcQO9hspw@discord.me4b4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

# Cryptography config

SECRET_KEY = "ced8b23cc52e496e9f9a6b24cc2b2b21a19224edc8a446a04bb525b276078f10eef5c1e827e2961197887b47900a37752af34a254718539967ed2ac56dab7ade04c83547b8c081a3f3bbdfdbdb7c82de309d922c3edd0e48603c2a9d4419fb2558886f40d8baed31f70c038702782a080085a264c6a4076b0a2729a2a8bf8f4cfdfa1e3cf24b1879c9dae70bef916a1cff671f39a6ca8b702db008881d1d28584a47c7665a948c88c1957d4009852c2a39e40187985c6672d426c9fd830ddbdf0e310057a629cfa8b918c0fbeb8dd1d8e1a2eb9e3b4ade55ecddfe6050f3df6e5c790a7729aa90a847681fa5e64926131c9071a7cf503b6f73968f2ffe710cf6"
ALGORITHM = "HS256"
CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

SCHEMES = ["bcrypt"]
DEPRECIATED = "auto"