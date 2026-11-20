from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager
from sqlalchemy import select
from src.database import engine, Base, AsyncSessionLocal
from src.models import User
from src.config import settings
from src.security import encrypt_password

from src.auth.router import router as auth_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Async create table
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Перевірка та створення першого адміна
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).where(User.role == "admin"))
        admin_exists = result.scalars().first()

        if not admin_exists:
            logger.info("Створення базового адміністратора...")
            new_admin = User(
                full_name="Super Admin",
                login=settings.default_admin_login,
                protected_password=encrypt_password(settings.default_admin_password),
                role="admin",
                status="active"
            )
            db.add(new_admin)
            await db.commit()
            logger.info("Адміністратора успішно створено!")

    yield  # Server is work

    # close connect
    await engine.dispose()

app = FastAPI(title="Password Manager API", lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"message": "API is running."}

app.include_router(auth_router)
