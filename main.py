from fastapi import FastAPI, HTTPException
from models import users
from schemas import UserCreate, UserLogin
from passlib.context import CryptContext
from db import database, metadata, engine



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