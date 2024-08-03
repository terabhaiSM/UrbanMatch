from sqlalchemy import Column, String, Integer, Boolean, Text, Enum as SQLAEnum
from sqlalchemy.ext.declarative import declarative_base
import uuid
from enum import Enum
Base = declarative_base()

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class RelationshipPreferenceEnum(str, Enum):
    friendship = "friendship"
    relationship = "relationship"
    casual = "casual"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    bio = Column(Text)
    gender = Column(SQLAEnum(GenderEnum), nullable=False)
    relationship_preference = Column(SQLAEnum(RelationshipPreferenceEnum), nullable=False)
    interests = Column(Text)  # Comma-separated list of interests
    is_verified = Column(Boolean, default=False)
    email_verification_token = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"
