import random
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True  # this is optional field
    rating: Optional[int] = None  # this is fully optional


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


@app.get('/')
def root():
    return {'data': 'hello'}


@app.get('/posts')
def get_post():
    return {'data': my_posts}


@app.post('/createpost', status_code=status.HTTP_201_CREATED)  # change default status code
def create_post(payload: Post):
    print(payload)
    print(payload.title)
    print(payload.content)
    print(type(payload))
    print(type(payload.dict()))
    post_dict = payload.dict()
    post_dict['id'] = random.randrange(0, 10000)
    my_posts.append(post_dict)
    return my_posts


@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    print(id)
    for item in my_posts:
        if item['id'] == id:
            return item
        else:
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'message': 'not found'}
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')


@app.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = get_index(id)
    if index is not None:
        my_posts.pop(index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')


@app.put('/posts/{id}', status_code=status.HTTP_206_PARTIAL_CONTENT)
def update_post(id: int, post: Post):
    index = get_index(id)
    print(index)
    if index is not None:
        update = post.dict()
        my_posts[index] = update
        return {'data': update}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
