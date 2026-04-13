from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate



class UserService:
    """Сервис для работы с полозователями """

    @staticmethod
    def create_user(db: Session, user_data: UserCreate):
        """Создать нового пользователя"""

        db_user = User(
            username = user_data.username,
            email = user_data.email
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user_by_id(db:Session, user_id: int):
        """Получить пользователя по ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db:Session, user_email: str):
        """Получить пользователя по ID"""
        return db.query(User).filter(User.email == user_email).first()
    
    def get_all_users(db: Session, skip: int = 0, limit:int = 100):
        """Получить всех пользователей (с пагинацией)"""
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_username(db: Session, user_id: int, new_username: str):  
        """Переименовать пользователя"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.username = new_username
            db.commit()
            db.refresh(user)
            return user
        return None
    
    def delete_user(db: Session, user_id: int):
        """Удалить пользователя"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
    
        
    
