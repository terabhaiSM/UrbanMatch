from pydantic import BaseModel
from typing import Optional
from enum import Enum

class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class RelationshipPreferenceEnum(str, Enum):
    FRIENDSHIP = "friendship"
    DATING = "dating"
    SERIOUS_RELATIONSHIP = "serious_relationship"

class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    bio: Optional[str]
    gender: GenderEnum
    relationship_preference: RelationshipPreferenceEnum
    location: str
    interests: Optional[str]
    is_verified: bool

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    age: Optional[int]
    bio: Optional[str]
    gender: Optional[GenderEnum]
    relationship_preference: Optional[RelationshipPreferenceEnum]
    location: Optional[str]
    interests: Optional[str]
    is_verified: Optional[bool]

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    age: int
    bio: Optional[str]
    gender: GenderEnum
    relationship_preference: RelationshipPreferenceEnum
    location: str
    interests: Optional[str]

    class Config:
        orm_mode = True
