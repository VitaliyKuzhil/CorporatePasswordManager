from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.auth.dependencies import get_current_user, get_current_admin
from src.database import get_db
from src.models import Service, Credential, User
from src.credentials.schemas import ServiceCreate, ServiceUpdate, ServiceResponse

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("/", response_model=list[ServiceResponse])
async def list_services(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Service).order_by(Service.service_name))
    services = result.scalars().all()

    response = []
    for service in services:
        count_result = await db.execute(
            select(func.count(Credential.credential_id)).where(Credential.service_id == service.service_id)
        )
        count = count_result.scalar()
        response.append(ServiceResponse(
            service_id=service.service_id,
            service_name=service.service_name,
            service_url=service.service_url,
            service_logo_url=service.service_logo_url,
            credential_count=count,
        ))
    return response


@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service(
    service_data: ServiceCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    service = Service(
        service_name=service_data.service_name,
        service_url=service_data.service_url,
        service_logo_url=service_data.service_logo_url,
    )
    db.add(service)
    await db.commit()
    await db.refresh(service)

    return ServiceResponse(
        service_id=service.service_id,
        service_name=service.service_name,
        service_url=service.service_url,
        service_logo_url=service.service_logo_url,
        credential_count=0,
    )


@router.put("/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: int,
    service_data: ServiceUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    result = await db.execute(select(Service).where(Service.service_id == service_id))
    service = result.scalars().one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Джерело не знайдено")

    if service_data.service_name is not None:
        service.service_name = service_data.service_name
    if service_data.service_url is not None:
        service.service_url = service_data.service_url
    if service_data.service_logo_url is not None:
        service.service_logo_url = service_data.service_logo_url

    await db.commit()
    await db.refresh(service)

    count_result = await db.execute(
        select(func.count(Credential.credential_id)).where(Credential.service_id == service.service_id)
    )
    count = count_result.scalar()

    return ServiceResponse(
        service_id=service.service_id,
        service_name=service.service_name,
        service_url=service.service_url,
        service_logo_url=service.service_logo_url,
        credential_count=count,
    )


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    service_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    result = await db.execute(select(Service).where(Service.service_id == service_id))
    service = result.scalars().one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Джерело не знайдено")

    await db.delete(service)
    await db.commit()
