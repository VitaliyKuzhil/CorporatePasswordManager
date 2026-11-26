from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
import pyotp

from src.config import settings
from src.models import AuthStrategyType


def pad_totp_secret(secret: str) -> str:
    """Доповнює короткий TOTP-секрет до мінімальної довжини для pyotp (112 біт = 24 символи Base32)."""
    clean = secret.strip().upper().replace(" ", "")
    # Google/Notion видають 16 символів (80 біт), але pyotp 2.9.0+ вимагає 112 біт.
    # Base32 вимагає довжини кратної 8. 24 символи = 15 байт = 120 біт.
    # Доповнюємо нульовими байтами ('A' у Base32) зправа для сумісності.
    if len(clean) < 24:
        clean = clean.ljust(24, 'A')
    return clean


class AccessStrategy(ABC):
    """Базовий інтерфейс стратегії доступу до сервісу."""

    @abstractmethod
    def prepare_access_payload(self, user, service, credential, decrypted_password: str, decrypted_totp_secret: str | None) -> dict:
        """Формує дані для фронтенду залежно від типу сервісу."""
        pass


class Password2FAStrategy(AccessStrategy):
    """Стратегія для зовнішніх сайтів: Пароль + живий 2FA код (TOTP)."""

    def prepare_access_payload(self, user, service, credential, decrypted_password: str, decrypted_totp_secret: str | None) -> dict:
        totp_code = None
        if decrypted_totp_secret:
            padded_secret = pad_totp_secret(decrypted_totp_secret)
            totp = pyotp.TOTP(padded_secret, interval=30)
            totp_code = totp.now()  # Генерує актуальний 6-значний код (кожні 30 сек)

        return {
            "strategy": "password_2fa",
            "login": credential.login,
            "password": decrypted_password,
            "totp_code": totp_code,
            "url": service.service_url,
        }


class SSOLinkStrategy(AccessStrategy):
    """Стратегія для корпоративних сервісів: Вхід за одноразовою JWT-перепусткою."""

    def prepare_access_payload(self, user, service, credential, decrypted_password: str, decrypted_totp_secret: str | None) -> dict:
        if not service.service_url:
            raise ValueError("SSO callback URL is not configured")
        payload = {
            "sub": user.login,
            "service_id": service.service_id,
            "aud": service.service_url,
            "jti": str(uuid4()),
            "exp": datetime.now(timezone.utc) + timedelta(seconds=30),
            "iss": "corporate-password-manager",
        }
        sso_token = jwt.encode(payload, settings.sso_secret_key, algorithm="HS256")

        return {
            "strategy": "sso_link",
            "redirect_url": service.service_url,
            "sso_token": sso_token,
        }


class StrategyContext:
    """Фабрика / Реєстр стратегій доступу."""

    _strategies = {
        AuthStrategyType.PASSWORD_2FA: Password2FAStrategy(),
        AuthStrategyType.SSO_LINK: SSOLinkStrategy(),
    }

    @classmethod
    def get_strategy(cls, auth_type: AuthStrategyType) -> AccessStrategy:
        strategy = cls._strategies.get(auth_type)
        if not strategy:
            raise ValueError(f"Непідтримуваний тип стратегії: {auth_type}")
        return strategy
