from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./app/db.sqlite3"
    broker_url: str = "redis://redis:6379/0"
    result_backend: str = "redis://redis:6379/0"

    healthcare_weight: float = 0.25
    education_weight: float = 0.25
    legal_access_weight: float = 0.25
    gender_equality_weight: float = 0.25

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

