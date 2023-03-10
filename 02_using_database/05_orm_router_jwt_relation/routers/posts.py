from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

import manage_jwt
import models
import schemas
from database_manager import get_db


router = APIRouter(
    tags=["posts"]
)


@router.get('/posts')
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post('/createpost', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)  # change default status code
def create_post(payload: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(manage_jwt.get_current_user)
                ):
    # new_post = models.Post(title=payload.title, content=payload.content, published=payload.published)
    new_post = models.Post(owner_id=current_user.id, **payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # like RETURNING in sql statement
    return new_post


@router.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    else:
        post_query.delete(synchronize_session=False)
        db.commit()


@router.put('/posts/{id}', status_code=status.HTTP_206_PARTIAL_CONTENT)
def update_post(id: int, payload: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is not None:
        post_query.update(payload.dict(), synchronize_session=False)
        db.commit()
        return post_query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
