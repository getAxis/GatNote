from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NoteCreate(BaseModel):
    """Схема для создания заметки"""
    title: str
    content: str

class NoteUpdate(BaseModel):
    """Схема для обновления заметки"""
    title: Optional[str] = None
    content: Optional[str] = None


class NoteResponse(BaseModel):
    """Схема для ответа"""
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True