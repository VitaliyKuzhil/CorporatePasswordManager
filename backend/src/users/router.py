
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user, get_current_admin
from src.database import get_db
from src.security import encrypt_password
from src.models import User, UserCredentialAccess, Service, Credential
from src.users.schemas import UserResponse, UserCreate, UserUpdateStatus, UpdateEmployee, EmployeeCredentialsResponse, GrantEmployeeCredentialRequest, GrantAllCredentialsRequest

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
async def list_users_for_admin(
    search: str = "",
    status_filter: str = "",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Отримати список усіх користувачів для адміністратора з пошуком та фільтром (без адмінів)."""
    query = select(User, func.count(UserCredentialAccess.user_id).label("access_count")) \
        .outerjoin(UserCredentialAccess,
            (User.user_id == UserCredentialAccess.user_id) &
            (UserCredentialAccess.is_active == True)
        ) \
        .where(User.role != "admin") \
        .group_by(User.user_id)

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (User.full_name.ilike(search_pattern)) |
            (User.login.ilike(search_pattern)) |
            (User.phone.ilike(search_pattern))
        )
    
    if status_filter:
        query = query.where(User.status == status_filter)
    
    query = query.order_by(User.full_name)
    result = await db.execute(query)
    rows = result.all()
    
    users_list = []
    for user, access_count in rows:
        users_list.append(UserResponse(
            user_id=user.user_id,
            full_name=user.full_name,
            login=user.login,
            phone=user.phone,
            avatar_url=user.avatar_url,
            role=user.role,
            status=user.status,
            access_count=access_count
        ))
    return users_list


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Створити нового користувача (тільки адміністратор)."""
    # Перевірка унікальності логіну
    existing = await db.execute(select(User).where(User.login == user_data.login))
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="Користувач з таким логіном вже існує")
    
    hashed = encrypt_password(user_data.password)
    new_user = User(
        full_name=user_data.full_name,
        login=user_data.login,
        protected_password=hashed,
        phone=user_data.phone,
        avatar_url=user_data.avatar_url,
        role=user_data.role,
        status=user_data.status,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return UserResponse(
        user_id=new_user.user_id,
        full_name=new_user.full_name,
        login=new_user.login,
        phone=new_user.phone,
        avatar_url=new_user.avatar_url,
        role=new_user.role,
        status=new_user.status,
        access_count=0
    )


@router.patch("/{user_id}")
async def update_employee(
    user_id: int,
    update_data: UpdateEmployee,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Оновити дані працівника (тільки адміністратор)."""
    user = await db.execute(select(User).where(User.user_id == user_id))
    user = user.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")

    # Перевірка унікальності логіну, якщо він змінюється
    if update_data.login is not None and update_data.login != user.login:
        existing = await db.execute(select(User).where(User.login == update_data.login))
        if existing.scalars().first():
            raise HTTPException(status_code=400, detail="Користувач з таким логіном вже існує")
        user.login = update_data.login

    # Зміна пароля, якщо надано
    if update_data.password is not None:
        user.protected_password = encrypt_password(update_data.password)

    # Оновлення ПІБ
    if update_data.full_name is not None:
        user.full_name = update_data.full_name

    # Оновлення телефону
    if update_data.phone is not None:
        user.phone = update_data.phone

    await db.commit()
    await db.refresh(user)

    return {"ok": True, "user_id": user.user_id, "login": user.login, "full_name": user.full_name, "phone": user.phone}


@router.patch("/{user_id}/status")
async def update_user_status(
    user_id: int,
    status_data: UserUpdateStatus,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Змінити статус користувача (active/blocked)."""
    if status_data.status not in ("active", "blocked"):
        raise HTTPException(status_code=400, detail="Невірний статус")
    
    user = await db.execute(select(User).where(User.user_id == user_id))
    user = user.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    
    user.status = status_data.status
    await db.commit()
    return {"ok": True, "status": user.status}


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_detail(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Отримати деталі працівника (тільки адміністратор)."""
    user = await db.execute(select(User).where(User.user_id == user_id))
    user = user.scalars().one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    
    # Рахуємо кількість доступів
    access_count_result = await db.execute(
        select(func.count(UserCredentialAccess.user_id)).where(
            UserCredentialAccess.user_id == user_id,
            UserCredentialAccess.is_active == True
        )
    )
    access_count = access_count_result.scalar()
    
    return UserResponse(
        user_id=user.user_id,
        full_name=user.full_name,
        login=user.login,
        phone=user.phone,
        avatar_url=user.avatar_url,
        role=user.role,
        status=user.status,
        access_count=access_count
    )


@router.get("/{user_id}/credentials", response_model=list[EmployeeCredentialsResponse])
async def get_user_credentials(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Отримати список креденшалів працівника (тільки адміністратор)."""
    # Перевіряємо, що користувач існує
    user = await db.execute(select(User).where(User.user_id == user_id))
    user = user.scalars().one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    
    # Отримуємо всі активні доступи користувача
    access_result = await db.execute(
        select(UserCredentialAccess)
        .where(
            UserCredentialAccess.user_id == user_id,
            UserCredentialAccess.is_active == True
        )
    )
    accesses = access_result.scalars().all()
    
    credentials_list = []
    for access in accesses:
        # Отримуємо креденшал
        cred_result = await db.execute(
            select(Credential).where(Credential.credential_id == access.credential_id)
        )
        cred = cred_result.scalars().one_or_none()
        if not cred:
            continue
        
        # Отримуємо сервіс
        service_result = await db.execute(
            select(Service).where(Service.service_id == cred.service_id)
        )
        service = service_result.scalars().one_or_none()
        if not service:
            continue
        
        credentials_list.append(EmployeeCredentialsResponse(
            credential_id=cred.credential_id,
            service_id=service.service_id,
            service_name=service.service_name or '',
            service_url=service.service_url,
            service_logo_url=service.service_logo_url,
            login=cred.login or '',
            protected_password=cred.protected_password or '',
            comment=cred.comment,
        ))
    
    return credentials_list


@router.post("/{user_id}/credentials", status_code=status.HTTP_201_CREATED)
async def grant_employee_credential(
    user_id: int,
    cred_data: GrantEmployeeCredentialRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Надати доступ до сервісу працівнику (тільки адміністратор)."""
    # Перевіряємо, що користувач існує
    user = await db.execute(select(User).where(User.user_id == user_id))
    user = user.scalars().one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    
    # Перевіряємо, що сервіс існує
    service_result = await db.execute(select(Service).where(Service.service_id == cred_data.service_id))
    service = service_result.scalars().one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Джерело не знайдено")
    
    # Створюємо новий креденшал
    credential = Credential(
        service_id=cred_data.service_id,
        login=cred_data.login,
        protected_password=cred_data.password,  # TODO: шифрувати
        comment=cred_data.comment,
    )
    db.add(credential)
    await db.flush()
    
    # Надаємо доступ користувачу
    access = UserCredentialAccess(
        user_id=user_id,
        credential_id=credential.credential_id,
        is_active=True,
    )
    db.add(access)
    await db.commit()
    
    return {"message": "Доступ надано"}


@router.delete("/{user_id}/credentials/{credential_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_employee_credential(
    user_id: int,
    credential_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Забрати доступ до креденшала у працівника (тільки адміністратор)."""
    # Знаходимо запис доступу
    access_result = await db.execute(
        select(UserCredentialAccess).where(
            UserCredentialAccess.user_id == user_id,
            UserCredentialAccess.credential_id == credential_id,
            UserCredentialAccess.is_active == True
        )
    )
    access = access_result.scalars().one_or_none()
    if not access:
        raise HTTPException(status_code=404, detail="Доступ не знайдено")
    
    access.is_active = False
    await db.commit()


@router.post("/{user_id}/grant-all-credentials")
async def grant_all_credentials_to_user(
    user_id: int,
    grant_data: GrantAllCredentialsRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Надати всі паролі одного користувача іншому (тільки адміністратор)."""
    # Перевіряємо, що цільовий користувач існує
    target_user = await db.execute(select(User).where(User.user_id == user_id))
    target_user = target_user.scalars().one_or_none()
    if not target_user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    
    # Перевіряємо, що користувач-джерело існує
    source_user = await db.execute(select(User).where(User.user_id == grant_data.source_user_id))
    source_user = source_user.scalars().one_or_none()
    if not source_user:
        raise HTTPException(status_code=404, detail="Користувач-джерело не знайдено")
    
    # Отримуємо всі активні доступи користувача-джерела
    source_accesses = await db.execute(
        select(UserCredentialAccess)
        .where(
            UserCredentialAccess.user_id == grant_data.source_user_id,
            UserCredentialAccess.is_active == True
        )
    )
    accesses = source_accesses.scalars().all()
    
    granted_count = 0
    for access in accesses:
        # Перевіряємо, чи цільовий користувач вже має доступ до цього креденшала
        existing_access = await db.execute(
            select(UserCredentialAccess).where(
                UserCredentialAccess.user_id == user_id,
                UserCredentialAccess.credential_id == access.credential_id,
                UserCredentialAccess.is_active == True
            )
        )
        if existing_access.scalars().one_or_none():
            continue
        
        # Надаємо доступ
        new_access = UserCredentialAccess(
            user_id=user_id,
            credential_id=access.credential_id,
            is_active=True,
        )
        db.add(new_access)
        granted_count += 1
    
    if granted_count > 0:
        await db.commit()
    
    return {"message": f"Надано {granted_count} доступ(ів)"}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """Видалити користувача (тільки адміністратор)."""
    if user_id == current_user.user_id:
        raise HTTPException(status_code=400, detail="Неможливо видалити себе")
    
    user = await db.execute(select(User).where(User.user_id == user_id))
    user = user.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    
    await db.delete(user)
    await db.commit()
