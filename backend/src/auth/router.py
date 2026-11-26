from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.auth.schemas import Token, UserProfile, UpdateProfile
from src.database import get_db
from src.models import LoginAttempt, User
from src.security import create_access_token, encrypt_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    client_ip = request.client.host if request.client else "unknown"
    attempt_username = form_data.username[:100]
    cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(minutes=15)
    await db.execute(delete(LoginAttempt).where(LoginAttempt.attempted_at < cutoff))
    attempts_result = await db.execute(
        select(func.count(LoginAttempt.login_attempt_id)).where(
            LoginAttempt.username == attempt_username,
            LoginAttempt.client_ip == client_ip,
            LoginAttempt.attempted_at >= cutoff,
        )
    )
    if attempts_result.scalar_one() >= 5:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Забагато невдалих спроб. Спробуйте пізніше.",
            headers={"Retry-After": "900"},
        )

    result = await db.execute(select(User).where(User.login == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(user.protected_password, form_data.password):
        db.add(LoginAttempt(username=attempt_username, client_ip=client_ip))
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний логін або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.status == "blocked":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Обліковий запис заблоковано. Зверніться до адміністратора.",
        )

    await db.execute(
        delete(LoginAttempt).where(
            LoginAttempt.username == attempt_username,
            LoginAttempt.client_ip == client_ip,
        )
    )
    await db.commit()
    access_token = create_access_token(
        data={"sub": user.login, "uid": user.user_id, "role": user.role, "ver": user.auth_version}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/profile", response_model=UserProfile)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.user_id,
        "login": current_user.login,
        "full_name": current_user.full_name,
        "phone": current_user.phone,
        "avatar_url": current_user.avatar_url,
        "role": current_user.role,
        "status": current_user.status,
    }


@router.put("/profile", response_model=UserProfile)
async def update_profile(
    profile_data: UpdateProfile,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin" and (profile_data.login is not None or profile_data.password is not None):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Змінювати логін і пароль може лише адміністратор",
        )
    if profile_data.full_name is not None:
        current_user.full_name = profile_data.full_name
    if profile_data.phone is not None:
        current_user.phone = profile_data.phone
    if profile_data.avatar_url is not None:
        current_user.avatar_url = profile_data.avatar_url

    # Зміна логіну — тільки для адміністратора
    if profile_data.login is not None and profile_data.login.strip():
        login = profile_data.login.strip()
        if login != current_user.login:
            result = await db.execute(select(User).where(User.login == login))
            existing = result.scalar_one_or_none()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Такий логін вже існує",
                )
            current_user.login = login
            current_user.auth_version += 1

    # Зміна пароля — тільки для адміністратора
    if profile_data.password is not None and profile_data.password.strip():
        current_user.protected_password = encrypt_password(profile_data.password.strip())
        current_user.auth_version += 1

    await db.commit()
    await db.refresh(current_user)

    return {
        "id": current_user.user_id,
        "login": current_user.login,
        "full_name": current_user.full_name,
        "phone": current_user.phone,
        "avatar_url": current_user.avatar_url,
        "role": current_user.role,
        "status": current_user.status,
    }