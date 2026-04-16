from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    """Схема для создания пользователя"""
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Схема для ответа (что видит клиент)"""
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
