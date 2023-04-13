import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


class Settings:
    POSTGRES_USER: str = os.getenv('FSTR_DB_LOGIN', 'postgres')
    POSTGRES_PASSWORD: str = os.getenv('FSTR_DB_PASS', 'changeme')
    POSTGRES_SERVER: str = os.getenv('FSTR_DB_HOST', 'postgres')
    POSTGRES_PORT: str = os.getenv('FSTR_DB_PORT', 5432)
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'FSTR')
    DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'


settings = Settings()
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
