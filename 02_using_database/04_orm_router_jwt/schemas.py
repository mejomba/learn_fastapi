from datetime import datetime

from pydantic import BaseModel, EmailStr, SecretStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # this is optional field
    # rating: Optional[int] = None  # this is fully optional


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserCreateResponse(UserCreate):
    password: SecretStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserGetResponse(BaseModel):
    email: EmailStr
    created_at: datetime
    id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
