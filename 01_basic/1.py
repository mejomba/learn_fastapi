from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def root():
    return {'data': 'hellow'}


@app.get('/post')
def get_post():
    return {'data': 'this is your post'}
