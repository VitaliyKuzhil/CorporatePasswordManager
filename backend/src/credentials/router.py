from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.auth.dependencies import get_current_user, get_current_admin
from src.database import get_db
from src.models import Service, Credential, User, UserCredentialAccess
from src.credentials.schemas import ServiceCreate, ServiceUpdate, ServiceResponse, ServiceDetailResponse, CredentialWithAccess, CredentialCreate, CredentialResponse
from src.users.schemas import UserResponse, GrantAccessRequest

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


@router.get("/{service_id}/detail", response_model=ServiceDetailResponse)
async def get_service_detail(
    service_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Service).where(Service.service_id == service_id))
    service = result.scalars().one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Джерело не знайдено")

    # Отримуємо всі креденшали для цього сервісу
    creds_result = await db.execute(
        select(Credential).where(Credential.service_id == service_id).order_by(Credential.credential_id)
    )
    credentials = creds_result.scalars().all()

    # Для кожного креденшала рахуємо кількість доступів
    cred_list = []
    total_access = 0
    for cred in credentials:
        access_result = await db.execute(
            select(func.count(UserCredentialAccess.credential_id)).where(
                UserCredentialAccess.credential_id == cred.credential_id,
                UserCredentialAccess.is_active == True
            )
        )
        access_count = access_result.scalar()
        total_access += access_count
        cred_list.append(CredentialWithAccess(
            credential_id=cred.credential_id,
            login=cred.login,
            protected_password=cred.protected_password,
            comment=cred.comment,
            access_count=access_count,
        ))

    return ServiceDetailResponse(
        service_id=service.service_id,
        service_name=service.service_name or '',
        service_url=service.service_url,
        service_logo_url=service.service_logo_url,
        credential_count=len(credentials),
        access_count=total_access,
        credentials=cred_list,
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


@router.get("/{service_id}/credentials/{credential_id}/access", response_model=list[UserResponse])
async def get_credential_access(
    service_id: int,
    credential_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Отримати список користувачів, які мають доступ до конкретного пароля."""
    # Перевіряємо, що креденшал належить цьому сервісу
    cred_result = await db.execute(
        select(Credential).where(
            Credential.credential_id == credential_id,
            Credential.service_id == service_id
        )
    )
    credential = cred_result.scalars().one_or_none()
    if not credential:
        raise HTTPException(status_code=404, detail="Креденшал не знайдено")

    # Отримуємо користувачів з активним доступом
    result = await db.execute(
        select(User)
        .join(UserCredentialAccess, User.user_id == UserCredentialAccess.user_id)
        .where(
            UserCredentialAccess.credential_id == credential_id,
            UserCredentialAccess.is_active == True
        )
        .order_by(User.full_name)
    )
    users = result.scalars().all()
    return users


@router.post("/{service_id}/credentials/{credential_id}/access", status_code=status.HTTP_201_CREATED)
async def grant_credential_access(
    service_id: int,
    credential_id: int,
    request: GrantAccessRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """Надати доступ до пароля користувачу (тільки адміністратор)."""
    # Перевіряємо, що креденшал належить цьому сервісу
    cred_result = await db.execute(
        select(Credential).where(
            Credential.credential_id == credential_id,
            Credential.service_id == service_id
        )
    )
    credential = cred_result.scalars().one_or_none()
    if not credential:
        raise HTTPException(status_code=404, detail="Креденшал не знайдено")

    # Перевіряємо, що користувач існує
    user_result = await db.execute(select(User).where(User.user_id == request.user_id))
    user = user_result.scalars().one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Користувач не знайдено")

    # Перевіряємо, чи вже є активний доступ
    existing = await db.execute(
        select(UserCredentialAccess).where(
            UserCredentialAccess.user_id == request.user_id,
            UserCredentialAccess.credential_id == credential_id
        )
    )
    access = existing.scalars().one_or_none()

    if access:
        # Якщо запис існує, реактивуємо його (можливо, раніше був деактивовано)
        if access.is_active:
            raise HTTPException(status_code=400, detail="Доступ вже надано")
        access.is_active = True
    else:
        # Якщо запису немає, створюємо новий
        access = UserCredentialAccess(
            user_id=request.user_id,
            credential_id=credential_id,
            is_active=True,
        )
        db.add(access)

    await db.commit()
    return {"message": "Доступ надано"}


@router.delete("/{service_id}/credentials/{credential_id}/access/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_credential_access(
    service_id: int,
    credential_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """Забрати доступ до пароля у користувача (тільки адміністратор)."""
    # Перевіряємо, що креденшал належить цьому сервісу
    cred_result = await db.execute(
        select(Credential).where(
            Credential.credential_id == credential_id,
            Credential.service_id == service_id
        )
    )
    credential = cred_result.scalars().one_or_none()
    if not credential:
        raise HTTPException(status_code=404, detail="Креденшал не знайдено")

    # Знаходимо запис доступу
    result = await db.execute(
        select(UserCredentialAccess).where(
            UserCredentialAccess.user_id == user_id,
            UserCredentialAccess.credential_id == credential_id
        )
    )
    access = result.scalars().one_or_none()
    if not access:
        raise HTTPException(status_code=404, detail="Доступ не знайдено")

    await db.delete(access)
    await db.commit()


@router.post("/{service_id}/credentials", response_model=CredentialResponse, status_code=status.HTTP_201_CREATED)
async def create_credential(
    service_id: int,
    cred_data: CredentialCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """Створити новий пароль для сервісу (тільки адміністратор)."""
    # Перевіряємо, що сервіс існує
    service_result = await db.execute(select(Service).where(Service.service_id == service_id))
    service = service_result.scalars().one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Джерело не знайдено")

    # Створюємо креденшал
    credential = Credential(
        service_id=service_id,
        login=cred_data.login if cred_data.login else None,
        protected_password=cred_data.password,  # TODO: шифрувати пароль
        comment=cred_data.comment if cred_data.comment else None,
    )
    db.add(credential)
    await db.flush()  # Отримуємо credential_id

    # Надаємо доступ обраним користувачам
    for user_id in cred_data.user_ids:
        user_result = await db.execute(select(User).where(User.user_id == user_id))
        user = user_result.scalars().one_or_none()
        if user:
            access = UserCredentialAccess(
                user_id=user_id,
                credential_id=credential.credential_id,
                is_active=True,
            )
            db.add(access)

    await db.commit()
    await db.refresh(credential)

    return CredentialResponse(
        credential_id=credential.credential_id,
        login=credential.login,
        comment=credential.comment,
    )
