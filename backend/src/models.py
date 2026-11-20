from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(100))
    login: Mapped[Optional[str]] = mapped_column(String(50), unique=True, index=True)
    protected_password: Mapped[Optional[str]] = mapped_column(String(255), comment="AES-зашифрований пароль")
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(255), comment="Зберігаємо посилання (S3/сервер)")
    role: Mapped[Optional[str]] = mapped_column(String(20), default="user", comment="'admin' або 'user'")
    status: Mapped[Optional[str]] = mapped_column(String(20), default="active", comment="'active' або 'blocked'")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())

class Service(Base):
    __tablename__ = "services"

    service_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    service_name: Mapped[Optional[str]] = mapped_column(String(100))
    service_url: Mapped[Optional[str]] = mapped_column(String(255), comment="Посилання для швидкого переходу на сайт")
    service_logo_url: Mapped[Optional[str]] = mapped_column(String(255))

class Credential(Base):
    __tablename__ = "credentials"

    credential_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.service_id", ondelete="CASCADE"))
    login: Mapped[Optional[str]] = mapped_column(String(100))
    protected_password: Mapped[Optional[str]] = mapped_column(String(255), comment="AES-зашифрований пароль")
    comment: Mapped[Optional[str]] = mapped_column(Text)

class UserCredentialAccess(Base):
    __tablename__ = "user_credential_access"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    credential_id: Mapped[int] = mapped_column(ForeignKey("credentials.credential_id", ondelete="CASCADE"), primary_key=True)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, default=True, comment="Можливість тимчасово забрати доступ без видалення запису")
    granted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())
