from pydantic import BaseModel


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
