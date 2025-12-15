import uuid
from pydantic import BaseModel, field_serializer
from typing import List
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class WikiSearchItem(BaseModel):
    title: str
    summary : str | None
    url : str | None
    key: str | None = None  # only REST endpoint returns it, ideally should be compulsary

class WikiSearchResult(BaseModel):
    result: List[WikiSearchItem]

class ArticleCreate(BaseModel):
    title : str

class ArticleRead(BaseModel):
    id : int
    title: str
    url: str
    tags: List[str]

    class Config:
        from_attributes = True

    @field_serializer('id')
    def serialize_id(self, value: int) -> str:
        return str(value)
class ArticleUpdateTags(BaseModel):
    tags: List[str]
