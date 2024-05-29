from alembic import command
from alembic.config import Config

alembic_cfg = Config("alembic.ini")


def apply_migrations():
    command.upgrade(alembic_cfg, "head")
