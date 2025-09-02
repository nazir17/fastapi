from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from db import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(50), unique=True, nullable=False, index=True),
    Column("password", String(255))
)

reset_tokens = Table(
    "reset_tokens",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("token", String(255), unique=True, nullable=False),
    Column("expires_at", DateTime, nullable=False)
)
