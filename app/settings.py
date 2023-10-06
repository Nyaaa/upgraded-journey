from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    SERVER_HOST: str = 'http://127.0.0.1:8000'
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'changeme'
    DB_HOST: str = 'postgres'
    DB_PORT: int = 5432
    DB_NAME: str = 'FSTR'
    DATABASE_URL: str = (
        f'postgresql+asyncpg://'
        f'{DB_USER}:{DB_PASSWORD}@'
        f'{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )


settings = Settings()
