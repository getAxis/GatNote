from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.v1 import users, notes
from fastapi.middleware.cors import CORSMiddleware




# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)

# Создаем приложение - ЭТО КЛЮЧЕВАЯ ПЕРЕМЕННАЯ!
app = FastAPI(title="Notebook API", version="1.0.0")

# Подключаем роутеры
app.include_router(users.router)
app.include_router(notes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Notebook API"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Server is running"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)