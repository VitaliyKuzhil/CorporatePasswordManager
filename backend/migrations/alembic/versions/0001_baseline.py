"""Create missing tables from the SQLAlchemy metadata baseline."""

from alembic import op

from src.database import Base
from src import models

revision = "0001_baseline"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    pass