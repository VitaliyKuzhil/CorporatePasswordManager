"""Add credential security, access history, and audit-log columns."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect
from cryptography.fernet import InvalidToken

from src.security import decrypt_password, encrypt_password

revision = "0002_secure_storage"
down_revision = "0001_baseline"
branch_labels = None
depends_on = None


def _columns(table_name: str) -> set[str]:
    return {column["name"] for column in inspect(op.get_bind()).get_columns(table_name)}


def _foreign_key_columns(table_name: str) -> set[tuple[str, ...]]:
    return {
        tuple(foreign_key["constrained_columns"])
        for foreign_key in inspect(op.get_bind()).get_foreign_keys(table_name)
    }


def upgrade() -> None:
    if "auth_type" not in _columns("services"):
        op.add_column(
            "services",
            sa.Column(
                "auth_type",
                sa.Enum("password_2fa", "sso_link", name="authstrategytype"),
                nullable=False,
                server_default="password_2fa",
            ),
        )

    if "auth_version" not in _columns("users"):
        op.add_column("users", sa.Column("auth_version", sa.Integer(), nullable=False, server_default="0"))
    op.alter_column("users", "protected_password", existing_type=sa.String(length=255), type_=sa.Text(), existing_nullable=True)
    op.execute("UPDATE users SET role = 'user' WHERE role IS NULL OR role NOT IN ('admin', 'user')")
    op.execute("UPDATE users SET status = 'active' WHERE status IS NULL OR status NOT IN ('active', 'blocked')")
    op.alter_column("users", "role", existing_type=sa.String(length=20), nullable=False, server_default="user")
    op.alter_column("users", "status", existing_type=sa.String(length=20), nullable=False, server_default="active")
    existing_checks = {
        constraint.get("name") for constraint in inspect(op.get_bind()).get_check_constraints("users")
    }
    if "ck_users_role" not in existing_checks:
        op.create_check_constraint("ck_users_role", "users", "role IN ('admin', 'user')")
    if "ck_users_status" not in existing_checks:
        op.create_check_constraint("ck_users_status", "users", "status IN ('active', 'blocked')")

    if "totp_secret" not in _columns("credentials"):
        op.add_column("credentials", sa.Column("totp_secret", sa.String(length=64), nullable=True))

    if "granted_by" not in _columns("user_credential_access"):
        op.add_column("user_credential_access", sa.Column("granted_by", sa.Integer(), nullable=True))
    if ("granted_by",) not in _foreign_key_columns("user_credential_access"):
        op.create_foreign_key(
            "fk_user_credential_access_granted_by",
            "user_credential_access",
            "users",
            ["granted_by"],
            ["user_id"],
            ondelete="SET NULL",
        )
    if "revoked_at" not in _columns("user_credential_access"):
        op.add_column("user_credential_access", sa.Column("revoked_at", sa.DateTime(), nullable=True))
    op.execute("UPDATE user_credential_access SET is_active = TRUE WHERE is_active IS NULL")
    op.alter_column(
        "user_credential_access",
        "is_active",
        existing_type=sa.Boolean(),
        nullable=False,
        server_default=sa.true(),
    )

    op.alter_column("credentials", "protected_password", existing_type=sa.String(length=255), type_=sa.Text(), existing_nullable=True)
    op.alter_column("credentials", "totp_secret", existing_type=sa.String(length=64), type_=sa.Text(), existing_nullable=True)

    connection = op.get_bind()
    secret_columns = (
        ("users", "user_id", "protected_password"),
        ("credentials", "credential_id", "protected_password"),
        ("credentials", "credential_id", "totp_secret"),
    )
    for table_name, primary_key, column_name in secret_columns:
        rows = connection.execute(sa.text(f"SELECT {primary_key}, {column_name} FROM {table_name}")).all()
        for row_id, value in rows:
            if not value:
                continue
            try:
                decrypt_password(value)
            except InvalidToken:
                if value.startswith("gAAAA"):
                    raise RuntimeError(
                        f"Cannot decrypt an existing token in {table_name}.{column_name}; verify ENCRYPTION_KEY/ENCRYPTION_KEYS."
                    ) from None
                connection.execute(
                    sa.text(f"UPDATE {table_name} SET {column_name} = :value WHERE {primary_key} = :row_id"),
                    {"value": encrypt_password(value), "row_id": row_id},
                )


def downgrade() -> None:
    raise RuntimeError("Downgrade is not supported for irreversible secret-storage changes")