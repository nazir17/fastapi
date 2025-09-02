from sqlalchemy import Table, Column, Integer, String, MetaData
from db import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(50), unique=True, nullable=False, index=True),
    Column("password", String(255))
)