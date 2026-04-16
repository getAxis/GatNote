from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key-change-this-in-production"  # TODO: в .env!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 день

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверить пароль/Chek the password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash the password/Захешировать пароль"""
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    """Create the access (JWT) token"""
    to_encode =  data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    """Decode the JWT token/Расшифровать JWT токен"""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


