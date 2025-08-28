from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

app = FastAPI()

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

@app.get("/api/users", response_model=List[User])
def get_users():
    return users

@app.post("/api/users", response_model=User)
def create_user(user: UserBase):
    global next_id

    if any(u.email == user.email for u in users):
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

    users.append(new_user)
    next_id += 1
    return new_user

@app.get("/api/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for u in users:
        if u.id == user_id:
            return u
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/api/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_data: UserBase):
    for idx, u in enumerate(users):
        if u.id == user_id:
            if any(u2.email == updated_data.email and u2.id != user_id for u2 in users):
                raise HTTPException(status_code=400, detail="Email already exists")

            updated_user = User(
                id=u.id,
                first_name=updated_data.first_name,
                last_name=updated_data.last_name,
                email=updated_data.email,
                password=updated_data.password,
                status=updated_data.status,
                created_at=u.created_at,
                updated_at=datetime.now()
            )
            users[idx] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    for idx, u in enumerate(users):
        if u.id == user_id:
            users.pop(idx)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
