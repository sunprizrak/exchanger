import os
from pathlib import Path
from typing import List
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class DjangoConfig(BaseModel):
    secret_key: str
    debug: bool
    allowed_hosts: List[str]
    language_code: str
    time_zone: str


class DatabaseConfig(BaseModel):
    engine: str
    name: str
    user: str
    password: str
    host: str
    port: int


class TelegramBot(BaseModel):
    telegram_bot_token: str


class CeleryConfig(BaseModel):
    broker_url: str
    result_backend: str
    accept_content: str
    task_serializer: str
    result_serializer: str

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(os.path.join(BASE_DIR, '.env.template'), os.path.join(BASE_DIR, '.env')),
        case_sensitive=False,
        env_file_encoding="utf-8",
        env_nested_delimiter='__',
        env_prefix='APP_CONFIG__',
    )
    django: DjangoConfig
    db: DatabaseConfig
    tg: TelegramBot
    celery: CeleryConfig


settings = Settings()


if __name__ == '__main__':
    pass