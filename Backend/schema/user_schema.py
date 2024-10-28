from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: int
    username: str
    name: str
    password: str
