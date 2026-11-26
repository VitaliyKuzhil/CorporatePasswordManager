from datetime import datetime, timedelta, timezone
from cryptography.fernet import Fernet, MultiFernet
import jwt
import hmac
from src.config import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

cipher_suite = MultiFernet([
    Fernet(key.strip().encode())
    for key in [settings.encryption_key, *settings.encryption_keys.split(",")]
    if key.strip()
])

def encrypt_password(password: str) -> str:
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(protected_password: str) -> str:
    return cipher_suite.decrypt(protected_password.encode()).decode()

def verify_password(protected_password: str | None, password: str) -> bool:
    if not protected_password:
        return False
    try:
        decrypted = decrypt_password(protected_password)
    except Exception:
        return False
    return hmac.compare_digest(decrypted.encode("utf-8"), password.encode("utf-8"))

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    delta = expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + delta
    to_encode.update({"exp": int(expire.timestamp())})
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
