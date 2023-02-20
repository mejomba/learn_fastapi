from fastapi import FastAPI, Body

app = FastAPI()


@app.get('/')
def root():
    return {'data': 'hello'}


@app.get('/post')
def get_post():
    return {'data': 'this is your post'}


@app.post('/createpost')
def create_post(payload: dict = Body(...)):
    print(payload)