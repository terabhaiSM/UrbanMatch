from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    bio: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    bio: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    bio: Optional[str] = None

    class Config:
        orm_mode = True
