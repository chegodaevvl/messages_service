import logging
import os
import pathlib
import sys
from logging.config import fileConfig

import alembic  # type: ignore
from psycopg2 import DatabaseError  # type: ignore
from sqlalchemy import engine_from_config, pool

# we're appending the app directory to our path here so that we can import config easily
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from app.core.settings import settings  # noqa

# Alembic Config object, which provides access to values within the .ini file
config = alembic.context.config


from app.db.models import Base

target_metadata = Base.metadata

# Interpret the config file for logging
fileConfig(config.config_file_name)  # type: ignore
logger = logging.getLogger("alembic.env")


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode
    """
    # db_suffix = os.environ.get("DB_SUFFIX", "")
    db_url = settings.DATABASE_URL.replace("+asyncpg", "")
    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", str(db_url))

    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),  # type: ignore
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        alembic.context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with alembic.context.begin_transaction():
            alembic.context.run_migrations()


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    """
    db_suffix = os.environ.get("DB_SUFFIX", "")

    if "test" in db_suffix:
        raise DatabaseError(
            "Running testing migrations offline currently not permitted."
        )

    alembic.context.configure(url=settings.DATABASE_URL)

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


if alembic.context.is_offline_mode():
    logger.info("Running migrations offline")
    run_migrations_offline()
else:
    logger.info("Running migrations online")
    run_migrations_online()
