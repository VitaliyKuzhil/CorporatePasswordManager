from datetime import datetime, timedelta, timezone
from cryptography.fernet import Fernet
import jwt
from src.config import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 12

cipher_suite = Fernet(settings.encryption_key.encode())

def encrypt_password(password: str) -> str:
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(protected_password: str) -> str:
    return cipher_suite.decrypt(protected_password.encode()).decode()

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": int(expire.timestamp())})
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
