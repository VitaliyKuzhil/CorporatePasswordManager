from typing import Optional, Literal

from pydantic import BaseModel

from src.models import AuthStrategyType


class ServiceBase(BaseModel):
    service_name: str
    service_url: Optional[str] = None
    service_logo_url: Optional[str] = None
    auth_type: AuthStrategyType = AuthStrategyType.PASSWORD_2FA


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    service_name: Optional[str] = None
    service_url: Optional[str] = None
    service_logo_url: Optional[str] = None
    auth_type: Optional[AuthStrategyType] = None


class ServiceResponse(ServiceBase):
    service_id: int
    credential_count: int = 0

    class Config:
        from_attributes = True


class CredentialWithAccess(BaseModel):
    credential_id: int
    login: Optional[str] = None
    password: Optional[str] = None
    totp_secret: Optional[str] = None
    comment: Optional[str] = None
    access_count: int = 0

    class Config:
        from_attributes = True


class ServiceDetailResponse(BaseModel):
    service_id: int
    service_name: str
    service_url: Optional[str] = None
    service_logo_url: Optional[str] = None
    credential_count: int = 0
    access_count: int = 0
    auth_type: AuthStrategyType = AuthStrategyType.PASSWORD_2FA
    credentials: list[CredentialWithAccess] = []

    class Config:
        from_attributes = True


class CredentialCreate(BaseModel):
    login: Optional[str] = None
    password: str
    totp_secret: Optional[str] = None
    comment: Optional[str] = None
    user_ids: list[int] = []


class CredentialUpdate(BaseModel):
    """Оновлення існуючого credential."""
    login: Optional[str] = None
    password: Optional[str] = None
    totp_secret: Optional[str] = None
    comment: Optional[str] = None
    user_ids: Optional[list[int]] = None


class CredentialResponse(BaseModel):
    credential_id: int
    login: Optional[str] = None
    totp_secret: Optional[str] = None
    comment: Optional[str] = None

    class Config:
        from_attributes = True


class MyAccessCredential(BaseModel):
    """Креденшал у списку доступів користувача."""
    credential_id: int
    login: Optional[str] = None
    comment: Optional[str] = None

    class Config:
        from_attributes = True


class MyAccessService(BaseModel):
    """Сервіс у списку доступів користувача."""
    service_id: int
    service_name: str
    service_url: Optional[str] = None
    service_logo_url: Optional[str] = None
    auth_type: AuthStrategyType = AuthStrategyType.PASSWORD_2FA
    credentials: list[MyAccessCredential] = []

    class Config:
        from_attributes = True


# ——— Access Data schemas (результат стратегії доступу) ———

class Password2FAAccessData(BaseModel):
    """Відповідь для стратегії password_2fa."""
    strategy: Literal["password_2fa"]
    login: Optional[str] = None
    password: str = ""
    totp_code: Optional[str] = None
    url: Optional[str] = None


class SSOLinkAccessData(BaseModel):
    """Відповідь для стратегії sso_link."""
    strategy: Literal["sso_link"]
    redirect_url: str
    sso_token: str


class AccessDataResponse(BaseModel):
    """Універсальна відповідь endpoint'у access-data."""
    strategy: str
    login: Optional[str] = None
    password: Optional[str] = None
    totp_code: Optional[str] = None
    url: Optional[str] = None
    redirect_url: Optional[str] = None
    sso_token: Optional[str] = None
