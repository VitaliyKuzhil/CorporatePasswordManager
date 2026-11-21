
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user, get_current_admin
from src.database import get_db
from src.models import User
from src.users.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
async def list_users(
    search: str = "",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Отримати список активних користувачів з можливістю пошуку."""
    query = select(User).where(User.status == "active")
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (User.full_name.ilike(search_pattern)) |
            (User.login.ilike(search_pattern))
        )
    query = query.order_by(User.full_name)
    result = await db.execute(query)
    users = result.scalars().all()
    return users
