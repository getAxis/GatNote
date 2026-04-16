from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    """Схема для создания пользователя"""
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    """Схема для ответа (что видит клиент)"""
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
