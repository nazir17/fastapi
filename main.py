from fastapi import FastAPI, HTTPException
import storage_service as service

app = FastAPI()

@app.get("/api/users")
def get_users():
    return service.get_users()

@app.post("/api/users")
def create_user(user: service.UserBase):
    return service.create_user(user)

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/api/users/{user_id}")
def update_user(user_id: int, user: service.UserBase):
    updated_user = service.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    deleted_user = service.delete_user(user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user
