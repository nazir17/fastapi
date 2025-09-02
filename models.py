from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from db import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("email", String(50), unique=True, nullable=False),
    Column("password", String(255), nullable=False),
    Column("role", String(50), nullable=False, default="user"),
    Column("status", String(50), nullable=False, default="active")
)

reset_tokens = Table(
    "reset_tokens",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("token", String(255), unique=True, nullable=False),
    Column("expires_at", DateTime, nullable=False)
)
