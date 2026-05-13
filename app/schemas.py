
from datetime import datetime
from pydantic import BaseModel, EmailStr, conint , Field
from typing import Annotated, Optional


class CREATE(BaseModel):  
    title: str
    content: str
    published: Optional[bool] = True


class UserOut(BaseModel):
    id: int
    email: EmailStr  
    created_at: datetime

    class Config:
        orm_mode = True  


class Post(CREATE):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut 

    class Config:
        orm_mode = True    


class PostOut(BaseModel):
    Post:Post
    votes:int

    class Config:
        orm_mode = True
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]