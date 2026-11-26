from typing import Literal
from pydantic import BaseModel

class UserResponse(BaseModel):
    user_id: int
    full_name: str | None = None
    login: str | None = None
    phone: str | None = None
    avatar_url: str | None = None
    role: str | None = None
    status: str | None = None
    access_count: int = 0

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    full_name: str
    login: str
    password: str
    phone: str | None = None
    avatar_url: str | None = None
    role: Literal["admin", "user"] = "user"
    status: Literal["active", "blocked"] = "active"


class UserUpdateStatus(BaseModel):
    status: Literal["active", "blocked"]


class UpdateEmployee(BaseModel):
    """Оновлення даних працівника адміністратором."""
    full_name: str | None = None
    phone: str | None = None
    login: str | None = None
    password: str | None = None


class GrantAccessRequest(BaseModel):
    user_id: int


class EmployeeCredentialsResponse(BaseModel):
    """Креденшал працівника з інформацією про сервіс."""
    credential_id: int
    service_id: int
    service_name: str
    service_url: str | None = None
    service_logo_url: str | None = None
    login: str
    password: str
    comment: str | None = None

    class Config:
        from_attributes = True


class EmployeeLoginPasswordResponse(BaseModel):
    login: str
    password: str


class GrantEmployeeCredentialRequest(BaseModel):
    """Запит на надання доступу до сервісу працівнику."""
    credential_id: int


class GrantAllCredentialsRequest(BaseModel):
    """Запит на надання всіх паролів одного користувача іншому."""
    source_user_id: int
