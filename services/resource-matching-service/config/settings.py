from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./app/db.sqlite3"
    model_path: str = "./ai/matching.pkl"
    transformer_path: str = "./ai/transformer.pkl"
    knn_n_neighbors: int = 5

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
