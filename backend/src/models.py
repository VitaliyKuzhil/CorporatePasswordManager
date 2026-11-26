import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import CheckConstraint, String, Text, Boolean, ForeignKey, DateTime, Enum, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class AuthStrategyType(str, enum.Enum):
    """Тип стратегії автентифікації для сервісу."""
    PASSWORD_2FA = "password_2fa"  # Логін + Пароль + 6-значний TOTP код
    SSO_LINK = "sso_link"          # Прямий перехід за одноразовим JWT-токеном

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role IN ('admin', 'user')", name="ck_users_role"),
        CheckConstraint("status IN ('active', 'blocked')", name="ck_users_status"),
    )

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(100))
    login: Mapped[Optional[str]] = mapped_column(String(50), unique=True, index=True)
    protected_password: Mapped[Optional[str]] = mapped_column(Text, comment="Fernet-зашифрований пароль")
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(255), comment="Зберігаємо посилання (S3/сервер)")
    role: Mapped[str] = mapped_column(String(20), default="user", server_default="user", nullable=False, comment="'admin' або 'user'")
    status: Mapped[str] = mapped_column(String(20), default="active", server_default="active", nullable=False, comment="'active' або 'blocked'")
    auth_version: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())

class Service(Base):
    __tablename__ = "services"

    service_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    service_name: Mapped[Optional[str]] = mapped_column(String(100))
    service_url: Mapped[Optional[str]] = mapped_column(String(255), comment="Посилання для швидкого переходу на сайт")
    service_logo_url: Mapped[Optional[str]] = mapped_column(String(255))
    auth_type: Mapped[AuthStrategyType] = mapped_column(
        Enum(AuthStrategyType, values_callable=lambda x: [e.value for e in x]),
        default=AuthStrategyType.PASSWORD_2FA,
        nullable=False,
        comment="Тип автентифікації: password_2fa або sso_link"
    )

class Credential(Base):
    __tablename__ = "credentials"

    credential_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.service_id", ondelete="CASCADE"))
    login: Mapped[Optional[str]] = mapped_column(String(100))
    protected_password: Mapped[Optional[str]] = mapped_column(Text, comment="Fernet-зашифрований пароль")
    totp_secret: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="Fernet-зашифрований Base32 секрет TOTP")
    comment: Mapped[Optional[str]] = mapped_column(Text)

class UserCredentialAccess(Base):
    __tablename__ = "user_credential_access"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    credential_id: Mapped[int] = mapped_column(ForeignKey("credentials.credential_id", ondelete="CASCADE"), primary_key=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="Можливість тимчасово забрати доступ без видалення запису")
    granted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())
    granted_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.user_id", ondelete="SET NULL"))
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

class AuditLog(Base):
    __tablename__ = "audit_log"

    audit_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    actor_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.user_id", ondelete="SET NULL"))
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(64), nullable=False)
    resource_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

class LoginAttempt(Base):
    __tablename__ = "login_attempts"

    login_attempt_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    client_ip: Mapped[str] = mapped_column(String(45), nullable=False, index=True)
    attempted_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
