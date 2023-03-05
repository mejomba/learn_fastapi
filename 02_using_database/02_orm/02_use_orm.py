from fastapi import FastAPI, Response, status, HTTPException, Depends
import uvicorn
from sqlalchemy.orm import Session
import models
import schemas
from database_manager import engin, get_db
import utils

models.base.metadata.create_all(bind=engin)

app = FastAPI()


@app.get('/posts')
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post('/createpost', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)  # change default status code
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db)):
    # new_post = models.Post(title=payload.title, content=payload.content, published=payload.published)
    new_post = models.Post(**payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # like RETURNING in sql statement
    return new_post


@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')


@app.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    else:
        post_query.delete(synchronize_session=False)
        db.commit()


@app.put('/posts/{id}', status_code=status.HTTP_206_PARTIAL_CONTENT)
def update_post(id: int, payload: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is not None:
        post_query.update(payload.dict(), synchronize_session=False)
        db.commit()
        return post_query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/users/{id}', response_model=schemas.UserGetResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')

    return user


if __name__ == "__main__":
    uvicorn.run(f'{__name__}:app', reload=True)
