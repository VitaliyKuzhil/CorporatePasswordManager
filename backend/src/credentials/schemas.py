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
