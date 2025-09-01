from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user_db import UserDB
from schemas.user_schema import UserCreate, UserUpdate, UserLogin, UserSignup
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def create_user(db: Session, user: UserCreate):
    db_user = UserDB(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=pwd_context.hash(user.password),
        status=user.status
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email or Username already exists")
    return db_user

def get_users(db: Session):
    return db.query(UserDB).all()

def signup_user(db: Session, user: UserSignup):
    existing_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = pwd_context.hash(user.password)
    db_user = UserDB(
        first_name="",
        last_name="",
        email=f"{user.username}@example.com",
        username=user.username,
        password=hashed_password,
        status="active"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db: Session, user: UserLogin):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid Username or Password")

    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid Username or Password")

    return {"message": "Login Successful", "username": db_user.username}

def get_user(db: Session, user_id: int):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
