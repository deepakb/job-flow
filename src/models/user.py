from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    name: str
    skills: List[str] = Field(default_factory=list)
    preferences: dict = Field(default_factory=dict)

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    skills: Optional[List[str]] = None
    preferences: Optional[dict] = None

class UserInDB(UserBase):
    id: str
    is_active: bool = True
    is_verified: bool = False

class UserResponse(UserBase):
    id: str
    is_active: bool
    is_verified: bool

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: str
