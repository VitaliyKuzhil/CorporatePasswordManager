import asyncio

from cryptography.fernet import InvalidToken
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings
from src.security import decrypt_password, encrypt_password


async def migrate_secret_column(connection, table: str, primary_key: str, column: str) -> int:
    result = await connection.execute(text(f"SELECT {primary_key}, {column} FROM {table}"))
    rows = result.all()
    migrated = 0
    for row_id, value in rows:
        if not value:
            continue
        try:
            decrypt_password(value)
        except InvalidToken:
            if value.startswith("gAAAA"):
                raise RuntimeError(
                    f"Cannot decrypt an existing token in {table}.{column}; verify ENCRYPTION_KEY/ENCRYPTION_KEYS."
                ) from None
            await connection.execute(
                text(f"UPDATE {table} SET {column} = :value WHERE {primary_key} = :row_id"),
                {"value": encrypt_password(value), "row_id": row_id},
            )
            migrated += 1
    return migrated


async def main() -> None:
    engine = create_async_engine(settings.database_url)
    try:
        async with engine.begin() as connection:
            count = 0
            count += await migrate_secret_column(connection, "users", "user_id", "protected_password")
            count += await migrate_secret_column(connection, "credentials", "credential_id", "protected_password")
            count += await migrate_secret_column(connection, "credentials", "credential_id", "totp_secret")
        print(f"Encrypted {count} previously plaintext secret values.")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())