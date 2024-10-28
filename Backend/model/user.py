from sqlalchemy import Table, Column, Integer, String
from config.db import engine, meta_data

user = Table("users", meta_data,
             Column("id", Integer, primary_key=True),
             Column("username", String(255), nullable=False),
             Column("name", String(255), nullable=False),
             Column("password", String(255), nullable=False))

meta_data.create_all(engine)
