import time
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

from sqlalchemy.orm import Session

from . import models
from .database_manager import engin, get_db

models.base.metadata.create_all(bind=engin)

app = FastAPI()





class Post(BaseModel):
    title: str
    content: str
    publish: bool = True  # this is optional field
    rating: Optional[int] = None  # this is fully optional


@app.get('/sqlalcheme')
def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data': posts}


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='learn_fastapi', user='postgres', password='1',
                                cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print('connect to database.')
        break
    except Exception as err:
        print('connect to database fail')
        print(err)
        time.sleep(2)

my_posts = [{'title': 'post 1 title', 'content': "post 1 content", 'id': 1},
            {'title': 'post 2 title', 'content': "post 2 content", 'id': 2},
            {'title': 'post 3 title', 'content': "post 3 content", 'id': 3},
            ]

def get_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get('/posts')
def get_post():
    cur.execute("""SELECT * FROM post""")
    posts = cur.fetchall()
    return {'data': posts}


@app.post('/createpost', status_code=status.HTTP_201_CREATED)  # change default status code
def create_post(payload: Post):
    query = """INSERT INTO post (title, content, published) VALUES(%s, %s, %s) RETURNING *"""
    data = payload.title, payload.content, payload.publish
    cur.execute(query, data)
    new_post = cur.fetchone()
    conn.commit()
    return new_post


@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    query = """SELECT * FROM post WHERE post_id=(%s)"""
    data = id,
    cur.execute(query, data)
    post = cur.fetchone()
    if post:
        return {'data': post}
    else:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': 'not found'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')


@app.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    query = """DELETE FROM post WHERE post_id=(%s) RETURNING *"""
    data = id,
    cur.execute(query, data)
    deleted_post = cur.fetchone()
    conn.commit()
    if deleted_post:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')


@app.put('/posts/{id}', status_code=status.HTTP_206_PARTIAL_CONTENT)
def update_post(id: int, post: Post):
    query = """UPDATE post SET title=%s, content=%s, published=%s WHERE post_id=%s RETURNING *"""
    data = post.title, post.content, post.publish, id
    cur.execute(query, data)
    updated_post = cur.fetchone()
    conn.commit()

    if updated_post:
        return {'data': updated_post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
