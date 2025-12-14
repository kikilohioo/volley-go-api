# app/api/auth/schemas.py

from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, EmailStr
from app.api.user.schemas import UserResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: Optional[str] = 'bearer'
    user: UserResponse


class TokenData(BaseModel):
    id: str | None = None


class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    avatar_url: Optional[str] = None


class RegisterUserDTO:
    def __init__(self, email: str, password: str, full_name: str, avatar: UploadFile | None):
        self.email = email
        self.password = password
        self.full_name = full_name
        self.avatar = avatar
