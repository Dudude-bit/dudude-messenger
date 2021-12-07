import os

from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    ENV: str = 'development'
    DEBUG: bool = True
    APP_HOST: str = '0.0.0.0'
    APP_PORT: int = 8000
    DB_URL: AnyUrl = 'edgedb://localhost/'
    QUEUE_URL: AnyUrl = None