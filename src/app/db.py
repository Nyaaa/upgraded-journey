import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base


class Settings:
    POSTGRES_USER: str = os.getenv('FSTR_DB_LOGIN', 'postgres')
    POSTGRES_PASSWORD: str = os.getenv('FSTR_DB_PASS', 'changeme')
    POSTGRES_SERVER: str = os.getenv('FSTR_DB_HOST', 'postgres')
    POSTGRES_PORT: str = os.getenv('FSTR_DB_PORT', 5432)
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'FSTR')
    DATABASE_URL = f'postgresql+asyncpg://' \
                   f'{POSTGRES_USER}:{POSTGRES_PASSWORD}@' \
                   f'{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'


settings = Settings()
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


# Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
