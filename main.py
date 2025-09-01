from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.user_db import Base
from schemas.user_schema import UserCreate, UserUpdate, UserResponse, UserSignup, UserLogin
from services import user_db_service
from config import settings

DATABASE_URL = f"mysql+pymysql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_database}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/users-db/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_db_service.create_user(db, user)

@app.post("/api/users/signup/", response_model=UserResponse)
def signup_user(user: UserSignup, db: Session = Depends(get_db)):
    return user_db_service.signup_user(db, user)

@app.post("/api/users/login/")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    return user_db_service.login_user(db, user)

@app.get("/api/users-db/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return user_db_service.get_users(db)

@app.get("/api/users-db/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_db_service.get_user(db, user_id)

@app.put("/api/users-db/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return user_db_service.update_user(db, user_id, user)

@app.delete("/api/users-db/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_db_service.delete_user(db, user_id)
