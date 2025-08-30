import memory_storage as mem
import file_storage as fstore
from pydantic import BaseModel

STORAGE_TYPE = "memory"   

storage = mem if STORAGE_TYPE == "memory" else fstore

UserBase = storage.UserBase
User = storage.User

def get_users():
    return storage.get_users() if STORAGE_TYPE == "memory" else storage.get_users_file()

def create_user(user: BaseModel):
    return storage.create_user(user) if STORAGE_TYPE == "memory" else storage.create_user_file(user)

def get_user(user_id: int):
    return storage.get_user(user_id) if STORAGE_TYPE == "memory" else storage.get_user_file(user_id)

def update_user(user_id: int, user: BaseModel):
    return storage.update_user(user_id, user) if STORAGE_TYPE == "memory" else storage.update_user_file(user_id, user)

def delete_user(user_id: int):
    return storage.delete_user(user_id) if STORAGE_TYPE == "memory" else storage.delete_user_file(user_id)
