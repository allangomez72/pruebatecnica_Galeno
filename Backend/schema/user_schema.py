from pydantic import BaseModel
from typing import Optional
class UserSchema(BaseModel):
    id: Optional[str]
    username: str
    name: str
    password: str
