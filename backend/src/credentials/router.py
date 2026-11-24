from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import base64
import pyotp

from src.auth.dependencies import get_current_user, get_current_admin
from src.database import get_db
from src.models import Service, Credential, User, UserCredentialAccess, AuthStrategyType
from src.credentials.schemas import ServiceCreate, ServiceUpdate, ServiceResponse, ServiceDetailResponse, CredentialWithAccess, CredentialCreate, CredentialUpdate, CredentialResponse, MyAccessService, MyAccessCredential, AccessDataResponse
from src.strategies import StrategyContext
from src.security import decrypt_password
from src.users.schemas import UserResponse, GrantAccessRequest

router = APIRouter(prefix="/services", tags=["Services"])


def normalize_totp_secret(secret: str) -> str:
    """Нормалізує TOTP секрет: видаляє пробіли, перетворює на uppercase."""
    return secret.strip().upper().replace(" ", "")


def validate_totp_secret(secret: str) -> bool:
    """Перевіряє чи є секрет валідним Base32."""
    try:
        clean = normalize_totp_secret(secret)
        base64.b32decode(clean)
        return True
    except Exception:
        return False


@router.get("/my-access", response_model=list[MyAccessService])
async def get_my_access(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Отримати список усіх сервісів та паролів, доступних поточному користувачу."""
    # Отримуємо всі активні доступи користувача
    result = await db.execute(
        select(Service, Credential)
        .join(UserCredentialAccess, Credential.credential_id == UserCredentialAccess.credential_id)
        .join(Service, Credential.service_id == Service.service_id)
        .where(
            UserCredentialAccess.user_id == current_user.user_id,
            UserCredentialAccess.is_active == True
        )
        .order_by(Service.service_name, Credential.credential_id)
    )
    rows = result.all()

    # Групуємо по сервісах
    services_map: dict[int, dict] = {}
    for service, cred in rows:
        sid = service.service_id
        if sid not in services_map:
            services_map[sid] = {
                "service": service,
                "credentials": []
            }
        services_map[sid]["credentials"].append(cred)

    response = []
    for sid in sorted(services_map.keys()):
        entry = services_map[sid]
        service = entry["service"]
        creds = entry["credentials"]
        response.append(MyAccessService(
            service_id=sid,
            service_name=service.service_name or '',
            service_url=service.service_url,
            service_logo_url=service.service_logo_url,
            auth_type=service.auth_type,
            credentials=[
                MyAccessCredential(
                    credential_id=c.credential_id,
                    login=c.login,
                    protected_password=c.protected_password,
                    totp_secret=c.totp_secret,
                    comment=c.comment,
                )
                for c in creds
            ],
        ))
    return response


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
        auth_type=service_data.auth_type,
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
    if service_data.auth_type is not None:
        service.auth_type = service_data.auth_type

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
        auth_type=service.auth_type,
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
        auth_type=service.auth_type,
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


@router.delete("/{service_id}/credentials/{credential_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_credential(
    service_id: int,
    credential_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """Видалити пароль з сервісу (тільки адміністратор)."""
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

    # Видаляємо всі записи доступу до цього креденшала
    access_result = await db.execute(
        select(UserCredentialAccess).where(
            UserCredentialAccess.credential_id == credential_id
        )
    )
    accesses = access_result.scalars().all()
    for access in accesses:
        await db.delete(access)

    # Видаляємо сам креденшал
    await db.delete(credential)
    await db.commit()


@router.put("/{service_id}/credentials/{credential_id}", response_model=CredentialResponse)
async def update_credential(
    service_id: int,
    credential_id: int,
    cred_data: CredentialUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """Оновити пароль для сервісу (тільки адміністратор)."""
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

    # Отримуємо сервіс для перевірки auth_type
    service_result = await db.execute(select(Service).where(Service.service_id == service_id))
    service = service_result.scalars().one_or_none()

    # Оновлюємо логін
    if cred_data.login is not None:
        credential.login = cred_data.login if cred_data.login else None

    # Оновлюємо пароль (якщо надано)
    if cred_data.password is not None:
        credential.protected_password = cred_data.password

    # Оновлюємо коментар
    if cred_data.comment is not None:
        credential.comment = cred_data.comment if cred_data.comment else None

    # Оновлюємо TOTP-секрет
    if cred_data.totp_secret is not None:
        if cred_data.totp_secret:
            # Валідація вручну введеного секрету
            if not validate_totp_secret(cred_data.totp_secret):
                raise HTTPException(
                    status_code=400,
                    detail="Невалідний TOTP секрет. Секрет має бути Base32 рядком (наприклад, JBSWY3DPEHPK3PXP)"
                )
            credential.totp_secret = normalize_totp_secret(cred_data.totp_secret)
        else:
            credential.totp_secret = None
    elif service and service.auth_type == AuthStrategyType.PASSWORD_2FA and not credential.totp_secret:
        # Якщо це password_2fa сервіс і немає секрету, генеруємо автоматично
        credential.totp_secret = pyotp.random_base32()

    # Оновлюємо доступи користувачів (якщо надано)
    if cred_data.user_ids is not None:
        # Видаляємо старі доступи
        access_result = await db.execute(
            select(UserCredentialAccess).where(
                UserCredentialAccess.credential_id == credential_id
            )
        )
        for access in access_result.scalars().all():
            await db.delete(access)
        # Додаємо нові доступи
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
        totp_secret=credential.totp_secret,
        comment=credential.comment,
    )


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

    # Автоматично генеруємо TOTP-секрет для password_2fa, якщо не вказано
    totp_secret = cred_data.totp_secret
    if totp_secret:
        # Валідація вручну введеного секрету
        if not validate_totp_secret(totp_secret):
            raise HTTPException(
                status_code=400,
                detail="Невалідний TOTP секрет. Секрет має бути Base32 рядком (наприклад, JBSWY3DPEHPK3PXP)"
            )
        totp_secret = normalize_totp_secret(totp_secret)
    elif service.auth_type == AuthStrategyType.PASSWORD_2FA:
        totp_secret = pyotp.random_base32()

    # Створюємо креденшал
    credential = Credential(
        service_id=service_id,
        login=cred_data.login if cred_data.login else None,
        protected_password=cred_data.password,  # TODO: шифрувати пароль
        totp_secret=totp_secret,
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
        totp_secret=credential.totp_secret,
        comment=credential.comment,
    )


@router.get("/credentials/{cred_id}/access-data", response_model=AccessDataResponse)
async def get_credential_access_data(
    cred_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Отримати дані для доступу до креденшала (пароль + 2FA або SSO-посилання)."""
    # 1. Перевіряємо, чи має користувач активний доступ
    result = await db.execute(
        select(Credential)
        .join(UserCredentialAccess, Credential.credential_id == UserCredentialAccess.credential_id)
        .where(
            Credential.credential_id == cred_id,
            UserCredentialAccess.user_id == current_user.user_id,
            UserCredentialAccess.is_active == True
        )
    )
    credential = result.scalars().one_or_none()
    if not credential:
        raise HTTPException(status_code=403, detail="Доступ закрито адміністратором")

    # 2. Отримуємо сервіс
    service_result = await db.execute(
        select(Service).where(Service.service_id == credential.service_id)
    )
    service = service_result.scalars().one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Сервіс не знайдено")

    # 3. Розшифровуємо пароль (якщо він є і потрібен)
    decrypted_pwd = ""
    if credential.protected_password and service.auth_type == AuthStrategyType.PASSWORD_2FA:
        try:
            decrypted_pwd = decrypt_password(credential.protected_password)
        except Exception:
            decrypted_pwd = ""

    # 4. Отримуємо потрібну стратегію та формуємо відповідь
    strategy = StrategyContext.get_strategy(service.auth_type)
    access_data = strategy.prepare_access_payload(
        user=current_user,
        service=service,
        credential=credential,
        decrypted_password=decrypted_pwd
    )

    return access_data
