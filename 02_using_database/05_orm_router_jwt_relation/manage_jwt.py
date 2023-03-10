from jose import JWTError, jwt
from typing import Dict
from datetime import datetime, timedelta
import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database_manager import get_db
import models


ALGORITHM = "HS256"
TOKEN_PERIOD_MINUTES = 30
SECRET_KEY = "4ab0d976f9c6fca23b50ba10281bf417ca6ba58490a61d358b51381072113c9b"  # openssl rand -hex 32


def create_jwt_token(data: Dict):
    encode_data = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=TOKEN_PERIOD_MINUTES)
    encode_data.update({"exp": exp})
    print(encode_data)

    jwt_token = jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token


def verify_access_token(token: str, credentials_exception):
    try:
        token_decode = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = token_decode.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl='login')), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="could not valid credentials",
                                          headers={"WWW-Authenticate": "Bearer"}
                                          )
    token = verify_access_token(token=token, credentials_exception=credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.user_id).first()
    return user

