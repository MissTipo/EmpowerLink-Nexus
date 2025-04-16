# config/settings.py

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

