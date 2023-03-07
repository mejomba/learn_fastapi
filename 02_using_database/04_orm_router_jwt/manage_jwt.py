from jose import JWTError, jwt
from typing import Dict
from datetime import datetime, timedelta


ALGORITHM = "HS256"
TOKEN_PERIOD_MINUTES = 30
SECRET_KEY = "4ab0d976f9c6fca23b50ba10281bf417ca6ba58490a61d358b51381072113c9b"  # openssl rand -hex 32


def create_jwt_token(data: Dict):
    encode_data = data.copy()
    exp = datetime.now() + timedelta(minutes=TOKEN_PERIOD_MINUTES)
    encode_data.update({"exp": exp})
    print(encode_data)

    jwt_token = jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token

