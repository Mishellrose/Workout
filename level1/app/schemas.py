from pydantic import BaseModel,EmailStr
from typing import Optional
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int

class UpdateUser(BaseModel):
    name: Optional[str]
    age: Optional[int]


class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    password: str
    age: int

class RegisterUserOut(BaseModel):
    name: str
    email: EmailStr
    age: int
    class Config():
        orm_mode = True

class LoginUser(BaseModel):
    email: str
    password: str

class Token_data(BaseModel):
    id: Optional[int]=None

class Token(BaseModel):
    access_token: str
    token_type: str
    