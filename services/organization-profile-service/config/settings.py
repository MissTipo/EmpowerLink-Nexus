# config/settings.py
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://empower_org:strongpass@localhost/org_profile_db"
    JWT_SECRET: str = "your_super_secret_key"    # change this in production
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(env_file=".env")  # Load .env file if exists

settings = Settings()

