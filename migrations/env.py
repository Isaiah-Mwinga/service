from sqlalchemy import engine_from_config, pool
from alembic import context
import os

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Get database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost/service")

# Import models
from app.models import Base  # Ensure all models are imported

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL, target_metadata=Base.metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=Base.metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
