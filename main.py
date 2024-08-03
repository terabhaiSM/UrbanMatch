import json
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, Text, Enum as SQLAEnum
import uuid
from database import engine, SessionLocal, Base
from models import User, GenderEnum, RelationshipPreferenceEnum
from schemas import UserCreate, UserUpdate, UserResponse
from sentence_transformers import SentenceTransformer, util
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

Base = declarative_base()

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize the sentence-transformers model
model = SentenceTransformer('all-MiniLM-L6-v2')

def compare_bios(bio1: str, bio2: str) -> float:
    """
    Compare two bios using the Sentence Transformer model and return a similarity score between 0 and 100.
    """
    embeddings1 = model.encode(bio1, convert_to_tensor=True)
    embeddings2 = model.encode(bio2, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)
    similarity_score = cosine_scores.item() * 100  # Convert to percentage
    return similarity_score

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generate a verification token
    token = secrets.token_urlsafe()
    send_verification_email(user.email, token)
    
    return db_user

def send_verification_email(email: str, token: str):
    # Configure your email server and sender details here
    smtp_server = os.getenv("SERVER")

    smtp_port = 587
    smtp_user = os.getenv("USER_MAIL")
    smtp_password = os.getenv("USER_PASSWORD")

    sender_email = smtp_user
    recipient_email = email
    subject = "Email Verification"
    body = f"Please verify your email by clicking the following link: http://localhost:8000/verify-email?token={token}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

@app.post("/users/send-verification/")
def send_verification(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="User already verified")

    # Generate a token
    token = str(uuid.uuid4())
    user.email_verification_token = token
    db.commit()

    # Send verification email
    send_verification_email(user.email, token)
    
    return {"detail": "Verification email sent"}

@app.get("/verify-email/")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email_verification_token == token).first()
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid token")

    user.is_verified = True
    user.email_verification_token = None  # Clear the token after verification
    db.commit()

    return {"detail": "Email verified successfully"}

@app.get("/users/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    for attr, value in user.dict(exclude_unset=True).items():
        setattr(db_user, attr, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}

@app.get("/users/{user_id}/matches", response_model=list[UserResponse])
def find_matches(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    potential_matches = db.query(User).filter(User.id != user_id).all()
    matches = []

    for potential_match in potential_matches:
        age_difference = abs(user.age - potential_match.age)
        bio_similarity = compare_bios(user.bio, potential_match.bio)
        
        # Calculate interest similarity
        user_interests = set(user.interests.split(","))
        match_interests = set(potential_match.interests.split(","))
        common_interests = user_interests.intersection(match_interests)
        interest_similarity = len(common_interests) / max(len(user_interests), len(match_interests)) * 100

        # Example weight combination
        bio_weight = 0.4
        interest_weight = 0.4
        age_weight = 0.2

        match_score = (
            (bio_similarity * bio_weight) +
            (interest_similarity * interest_weight) -
            (age_difference * age_weight)
        )
        
        # Normalize and add the match if it scores above a threshold
        if match_score > 50:
            matches.append(potential_match)

    # Sort matches by score in descending order
    matches.sort(key=lambda x: x.match_score, reverse=True)
    
    return matches