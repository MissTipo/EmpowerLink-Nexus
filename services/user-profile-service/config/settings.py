# config/settings.py

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test_org.db"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

