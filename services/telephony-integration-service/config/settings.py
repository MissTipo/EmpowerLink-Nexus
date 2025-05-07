# telephony-integration-service/config/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    USSD_CODE: str = "*999#"
    IVR_NUMBER: str = "300"
    # The GraphQL endpoint of the user profile service. Adjust as needed.
    USER_PROFILE_GRAPHQL_URL: str = "http://user-profile:8001/graphql/"
    USSD_CALLBACK_URL= http://telephony-integration-service:8000/ussd

    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

