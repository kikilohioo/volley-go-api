# app/api/user/schemas.py

from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateUserRequest(BaseModel):
    full_name: str
    email: EmailStr
    role: str = Field(default='player')
    avatar_url: Optional[str] = None


class UpdateUserRequest(BaseModel):
    email: EmailStr
    full_name: str
    role: str = "player"
    avatar_url: Optional[str] = None
    status: bool = True


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str = Field(default='player')
    avatar_url: Optional[str] = None
    status: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateUserDTO:
    def __init__(
        self, 
        email: str | None = None, 
        password: str | None = None, 
        full_name: str | None = None, 
        avatar: UploadFile | None = None, 
        role: str | None = None
    ):
        self.email = email
        self.password = password
        self.full_name = full_name
        self.avatar = avatar
        self.role = role


class SetUserRoleRequest(BaseModel):
    role: str | None = Field(default='player')