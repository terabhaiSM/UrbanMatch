from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)  # Specify length for String
    email = Column(String(100), unique=True, nullable=False)  # Specify length for String
    age = Column(Integer, nullable=False)
    bio = Column(String(200))  # Specify length for String
