import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import get_db
from src.models import User
from src.security import ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не вдалося перевірити облікові дані",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        user_id = payload.get("uid")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    if user_id is not None:
        try:
            user_query = select(User).where(User.user_id == int(user_id))
        except (TypeError, ValueError):
            raise credentials_exception
    else:
        user_query = select(User).where(User.login == username)

    result = await db.execute(user_query)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    if payload.get("ver", 0) != user.auth_version:
        raise credentials_exception

    if user.status == "blocked":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Обліковий запис заблоковано. Зверніться до адміністратора.",
        )

    return user


async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостатньо прав доступу",
        )
    return current_user