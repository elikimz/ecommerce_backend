
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    id:int

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    address: str
    phone: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    address: str
    phone: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)





class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str


class UserUpdate(BaseModel):
    address: Optional[str] = None
    phone: Optional[str] = None