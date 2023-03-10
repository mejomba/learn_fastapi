from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models
import schemas
from database_manager import get_db
import utils
import manage_jwt


router = APIRouter(tags=["authentication"])


@router.post('/login', response_model=schemas.Token)
# def user_login(user_credentials: schemas.UserLogin ,db: Session = Depends(get_db)):  # send raw json
def user_login(user_credentials: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):  # send form data
    # user = db.query(models.User).filter(models.User.email == user_credentials.email).first()  # send raw json
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()  # send form data
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    token = manage_jwt.create_jwt_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}