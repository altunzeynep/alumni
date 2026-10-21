from logging.config import fileConfig
import os
from dotenv import load_dotenv

from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool

from alembic import context

# Projedeki modellerin MetaData'sını buraya bağlıyoruz (Otomatik tablo üretimi için şart)
from app.database import Base  # Projendeki Base tanımının yolu
from app.models import *       # Tüm modellerin yüklenmesi için

# .env dosyasını okumasını sağlıyoruz
load_dotenv()

config = context.config

# Loglama ayarları
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    # Docker ortamındaki veya .env'deki DATABASE_URL'i alır, yoksa varsayılanı kullanır
    return os.getenv("DATABASE_URL", "postgresql://postgres:password@postgres:5432/alumni_db")


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()