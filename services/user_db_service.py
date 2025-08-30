from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user_db import UserDB
from schemas.user_schema import UserCreate, UserUpdate

def create_user(db: Session, user: UserCreate):
    db_user = UserDB(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password,
        status=user.status
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    return db_user

def get_users(db: Session):
    return db.query(UserDB).all()

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
