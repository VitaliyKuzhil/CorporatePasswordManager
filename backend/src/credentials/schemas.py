from typing import Optional

from pydantic import BaseModel


class ServiceBase(BaseModel):
    service_name: str
    service_url: Optional[str] = None
    service_logo_url: Optional[str] = None


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    service_name: Optional[str] = None
    service_url: Optional[str] = None
    service_logo_url: Optional[str] = None


class ServiceResponse(ServiceBase):
    service_id: int
    credential_count: int = 0

    class Config:
        from_attributes = True


class CredentialWithAccess(BaseModel):
    credential_id: int
    login: Optional[str] = None
    protected_password: Optional[str] = None
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
    credentials: list[CredentialWithAccess] = []

    class Config:
        from_attributes = True


class CredentialCreate(BaseModel):
    login: Optional[str] = None
    password: str
    comment: Optional[str] = None
    user_ids: list[int] = []


class CredentialResponse(BaseModel):
    credential_id: int
    login: Optional[str] = None
    comment: Optional[str] = None

    class Config:
        from_attributes = True


class MyAccessCredential(BaseModel):
    """Креденшал у списку доступів користувача."""
    credential_id: int
    login: Optional[str] = None
    protected_password: Optional[str] = None
    comment: Optional[str] = None

    class Config:
        from_attributes = True


class MyAccessService(BaseModel):
    """Сервіс у списку доступів користувача."""
    service_id: int
    service_name: str
    service_url: Optional[str] = None
    service_logo_url: Optional[str] = None
    credentials: list[MyAccessCredential] = []

    class Config:
        from_attributes = True
