from fastapi import HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime
import json
import os



class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    status: str

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

users: List[User] = []
next_id = 1

FILE_PATH = "users.json"

def load_users_from_file() -> List[User]:
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        data = json.load(f)
        return [User(**u) for u in data]

def save_users_to_file(users: List[User]):
    with open(FILE_PATH, "w") as f:
        json.dump([u.model_dump() for u in users], f, default=str, indent=4)

def get_users_file():
    return load_users_from_file()

def create_user_file(user: UserBase):
    users_file = load_users_from_file()
    next_id = max([u.id for u in users_file], default=0) + 1

    if any(u.email == user.email for u in users_file):
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        id=next_id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password,
        status=user.status,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    users_file.append(new_user)
    save_users_to_file(users_file)
    return new_user

def get_user_file(user_id: int):
    users_file = load_users_from_file()
    for u in users_file:
        if u.id == user_id:
            return u
    raise HTTPException(status_code=404, detail="User not found")

def update_user_file(user_id: int, updated_data: UserBase):
    users_file = load_users_from_file()
    for idx, u in enumerate(users_file):
        if u.id == user_id:
            if any(u2.email == updated_data.email and u2.id != user_id for u2 in users_file):
                raise HTTPException(status_code=400, detail="Email already exists")

            updated_user = User(
                id=u.id,
                first_name=updated_data.first_name,
                last_name=updated_data.last_name,
                email=updated_data.email,
                password=updated_data.password,
                status=updated_data.status,
                created_at=u.created_at,
                updated_at=datetime.utcnow()
            )
            users_file[idx] = updated_user
            save_users_to_file(users_file)
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

def delete_user_file(user_id: int):
    users_file = load_users_from_file()
    for idx, u in enumerate(users_file):
        if u.id == user_id:
            users_file.pop(idx)
            save_users_to_file(users_file)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")