from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Кошачий благотворительный фонд (0.1.0)'
    description: str = 'Сервис для поддержки котиков!'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'default_secret'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None
    DEFAULT_AMOUNT = 0
    FORMAT_DATE = "%Y/%m/%d %H:%H:%S"
    GT_FOR_AMOUNT = 0
    GT_FOR_PASSWORD = 3
    LIFETIME_JWT_TOKEN = 3600
    LOCALE = 'ru_RU'
    MAX_LENGTH_NAME = 100
    MIN_LENGTH_NAME = 1
    MIN_LENGTH_DESCRIPTION = 1
    ROW_SHEETS = 100
    COLUMN_SHEETS = 3

    class Config:
        env_file = '.env'


settings = Settings()
