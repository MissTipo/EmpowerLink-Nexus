# config/settings.py

from typing import Optional
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = Field(default="sqlite:///./test_org.db")
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

