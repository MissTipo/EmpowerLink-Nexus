from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    USSD_CODE: str = "*999#"
    IVR_NUMBER: str = "300"
    USER_PROFILE_GRAPHQL_URL: str = "https://empowerlinknexus.me/graphql"
    GEOMAP_URL: str = "https://empowerlinknexus.me/graphql"
    USSD_CALLBACK_URL: str = "https://empowerlinknexus.me/ussd"

    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

