from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    password: str
    status: str = "active"

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    username: Optional[str]
    password: Optional[str]
    status: Optional[str]

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserSignup(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
