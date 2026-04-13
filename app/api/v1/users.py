from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Создать нового пользователя"""
    # Проверяем, не существует ли пользователь с таким email
    existing_user = UserService.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return UserService.create_user(db, user_data)

@router.get("/", response_model=List[UserResponse])
def get_all_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Получить всех пользователей"""
    return UserService.get_all_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Получить пользователя по ID"""
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Удалить пользователя"""
    if not UserService.delete_user(db, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )