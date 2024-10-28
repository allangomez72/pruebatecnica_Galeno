from sqlalchemy import Table, Column, Integer
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import engine, meta_data

product = Table("products", meta_data,
             Column("id", Integer, primary_key=True),
             Column("productname", String(255), nullable=False),
             Column("stock", String(255), nullable=False),
             Column("price", String(255), nullable=False))

meta_data.create_all(engine)