from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.note_service import NoteService
from app.services.user_service import UserService
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse

router = APIRouter(prefix="/notes", tags=["Заметки"])

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note_data: NoteCreate, 
    user_id: int,  # Временно передаем ID пользователя
    db: Session = Depends(get_db)
):
    """Создать заметку для пользователя"""
    # Проверяем, существует ли пользователь
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return NoteService.create_note(db, note_data, user_id)

@router.get("/user/{user_id}", response_model=List[NoteResponse])
def get_user_notes(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получить все заметки пользователя"""
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return NoteService.get_user_notes(db, user_id, skip=skip, limit=limit)

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """Получить заметку по ID"""
    note = NoteService.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return note

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_data: NoteUpdate,
    db: Session = Depends(get_db)
):
    """Обновить заметку"""
    note = NoteService.update_note(db, note_id, note_data)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """Удалить заметку"""
    if not NoteService.delete_note(db, note_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )