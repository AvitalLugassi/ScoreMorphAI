"""Alembic migration environment — place this file at data/app_data/migrations/env.py"""
import sys, os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Make core_service importable from this location
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend", "core_service"))

from database import Base, engine  # noqa: E402
from models import User, Arrangement  # noqa: F401, E402

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_online():
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
