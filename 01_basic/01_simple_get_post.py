from fastapi import FastAPI, Body
import uvicorn


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


if __name__ == "__main__":
    uvicorn.run(f'{__name__}:app', reload=True)