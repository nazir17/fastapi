from fastapi import FastAPI
import file_storage as fstore
import memory_storage as mem

app = FastAPI()

@app.get("/api/users")
def get_users():
    return mem.get_users()

@app.post("/api/users")
def create_user(user: mem.UserBase):
    return mem.create_user(user)

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    return mem.get_user(user_id)

@app.put("/api/users/{user_id}")
def update_user(user_id: int, user: mem.UserBase):
    return mem.update_user(user_id, user)

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    return mem.delete_user(user_id)

# endpoints of storage
@app.get("/api/users-files")
def get_users_file():
    return fstore.get_users_file()

@app.post("/api/users-files")
def create_user_file(user: fstore.UserBase):
    return fstore.create_user_file(user)

@app.get("/api/users-files/{user_id}")
def get_user_file(user_id: int):
    return fstore.get_user_file(user_id)

@app.put("/api/users-files/{user_id}")
def update_user_file(user_id: int, user: fstore.UserBase):
    return fstore.update_user_file(user_id, user)

@app.delete("/api/users-files/{user_id}")
def delete_user_file(user_id: int):
    return fstore.delete_user_file(user_id)