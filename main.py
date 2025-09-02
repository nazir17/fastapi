from fastapi import FastAPI, HTTPException
from models import users, reset_tokens
from schemas import UserCreate, UserLogin, ForgotPasswordRequest, ResetPasswordRequest
from passlib.context import CryptContext
from db import database, metadata, engine
from datetime import datetime, timedelta
import secrets

metadata.create_all(bind=engine)

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/api/users/signup/")
async def signup_user(user: UserCreate):
    query = users.select().where(users.c.email == user.email)
    existing_user = await database.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = pwd_context.hash(user.password)
    query = users.insert().values(email=user.email, password=hashed_password)
    await database.execute(query)
    return {"message": "User registered successfully"}

@app.post("/api/users/login/")
async def login_user(user: UserLogin):
    query = users.select().where(users.c.email == user.email)
    existing_user = await database.fetch_one(query)
    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid email")

    if not pwd_context.verify(user.password, existing_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid password")

    return {"message": "Login Successful"}

@app.post("/api/users/forgot-password/")
async def forgot_password(request: ForgotPasswordRequest):
    query = users.select().where(users.c.email == request.email)
    user = await database.fetch_one(query)
    if not user:
        raise HTTPException(status_code=400, detail="Email not found")

    token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(minutes=10)

    insert_query = reset_tokens.insert().values(
        user_id=user["id"],
        token=token,
        expires_at=expires_at
    )
    await database.execute(insert_query)

    print(f"Password reset link: http://localhost:8000/api/users/reset-password/?token={token}")

    return {"message": "Password reset link has been sent to your email"}

@app.post("/api/users/reset-password/")
async def reset_password(request: ResetPasswordRequest):
    query = reset_tokens.select().where(reset_tokens.c.token == request.token)
    token_data = await database.fetch_one(query)

    if not token_data:
        raise HTTPException(status_code=400, detail="Invalid token")

    if token_data["expires_at"] < datetime.now():
        raise HTTPException(status_code=400, detail="Token expired")

    hashed_password = pwd_context.hash(request.new_password)

    update_query = users.update().where(users.c.id == token_data["user_id"]).values(password=hashed_password)
    await database.execute(update_query)

    delete_query = reset_tokens.delete().where(reset_tokens.c.id == token_data["id"])
    await database.execute(delete_query)

    return {"message": "Password reset successful"}
