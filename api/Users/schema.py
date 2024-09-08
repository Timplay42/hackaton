from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UsersBase(BaseModel):
    name: str
    last_name: str
    username: str
    password: bytes
    email: Optional[EmailStr] = None
    role: str

class UsersCreate(BaseModel):
    name: str
    last_name: str
    username: str
    password: str

class UsersLogin(BaseModel):
    username: str
    password: str

class UsersResponse(UsersCreate):
    pass

