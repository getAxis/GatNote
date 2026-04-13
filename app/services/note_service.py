from sqlalchemy.orm import Session
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate

class NoteService:
    """Сервис для работы с заметками"""
    
    @staticmethod
    def create_note(db: Session, note_data: NoteCreate, user_id: int):
        """Создать заметку для пользователя"""
        db_note = Note(
            title=note_data.title,
            content=note_data.content,
            user_id=user_id
        )
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note
    
    @staticmethod
    def get_note_by_id(db: Session, note_id: int):
        """Получить заметку по ID"""
        return db.query(Note).filter(Note.id == note_id).first()
    
    @staticmethod
    def get_user_notes(db: Session, user_id: int, skip: int = 0, limit: int = 100):
        """Получить все заметки пользователя"""
        return db.query(Note).filter(Note.user_id == user_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_note(db: Session, note_id: int, note_data: NoteUpdate):
        """Обновить заметку"""
        note = db.query(Note).filter(Note.id == note_id).first()
        if note:
            # Обновляем только те поля, которые пришли
            if note_data.title is not None:
                note.title = note_data.title
            if note_data.content is not None:
                note.content = note_data.content
            db.commit()
            db.refresh(note)
        return note
    
    @staticmethod
    def delete_note(db: Session, note_id: int):
        """Удалить заметку"""
        note = db.query(Note).filter(Note.id == note_id).first()
        if note:
            db.delete(note)
            db.commit()
            return True
        return False