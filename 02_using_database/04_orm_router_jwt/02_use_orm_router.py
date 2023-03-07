from fastapi import FastAPI
import uvicorn
import models
from database_manager import engin

from routers import posts, users, auth

models.base.metadata.create_all(bind=engin)

app = FastAPI()


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


if __name__ == "__main__":
    uvicorn.run(f'{__name__}:app', reload=True)
