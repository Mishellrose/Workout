from pydantic import BaseModel,EmailStr
from typing import Optional
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int

class UpdateUser(BaseModel):
    name: Optional[str]
    age: Optional[int]


