import time
# import psycopg2
# from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import uvicorn

from sqlalchemy.orm import Session

import models
from database_manager import engin, get_db

models.base.metadata.create_all(bind=engin)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # this is optional field
    # rating: Optional[int] = None  # this is fully optional


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='learn_fastapi', user='postgres', password='1',
#                                 cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         print('connect to database.')
#         break
#     except Exception as err:
#         print('connect to database fail')
#         print(err)
#         time.sleep(2)

my_posts = [{'title': 'post 1 title', 'content': "post 1 content", 'id': 1},
            {'title': 'post 2 title', 'content': "post 2 content", 'id': 2},
            {'title': 'post 3 title', 'content': "post 3 content", 'id': 3},
            ]


def get_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get('/posts')
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data': posts}


@app.post('/createpost', status_code=status.HTTP_201_CREATED)  # change default status code
def create_post(payload: Post, db: Session = Depends(get_db)):
    # new_post = models.Post(title=payload.title, content=payload.content, published=payload.published)
    new_post = models.Post(**payload.dict())
    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # like RETURNING in sql statement
    return new_post


@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if post:
        return {'data': post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')


@app.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    print(post)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    else:
        post_query.delete(synchronize_session=False)
        db.commit()


@app.put('/posts/{id}', status_code=status.HTTP_206_PARTIAL_CONTENT)
def update_post(id: int, payload: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is not None:
        post_query.update(payload.dict(), synchronize_session=False)
        db.commit()
        return {'data': post_query.first()}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')


if __name__ == "__main__":
    uvicorn.run(f'{__name__}:app', reload=True)
