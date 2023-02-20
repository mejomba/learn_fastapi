import random

from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True  # this is optional field
    rating: Optional[int] = None  # this is fully optional


my_posts = [{'title': 'post 1 title', 'content': "post 1 content", 'id': 1},
            {'title': 'post 2 title', 'content': "post 2 content", 'id': 2},
            {'title': 'post 3 title', 'content': "post 3 content", 'id': 3},
            ]


@app.get('/')
def root():
    return {'data': 'hello'}


@app.get('/posts')
def get_post():
    return {'data': my_posts}


@app.post('/createpost')
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
def get_post(id: int):
    print(id)
    for item in my_posts:
        if item['id'] == id:
            return item
