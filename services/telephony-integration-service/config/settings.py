# telephony-integration-service/config/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    USSD_CODE: str = "*999#"
    IVR_NUMBER: str = "300"
    # The GraphQL endpoint of the user profile service. Adjust as needed.
    USER_PROFILE_GRAPHQL_URL: str = "http://159.203.54.10.nip.io/graphql"
    USSD_CALLBACK_URL: str = "http://telephony-integration:8003/graphql/"
    # USSD_CALLBACK_URL: str = "http://159.203.54.10.nip.io/ussd"

    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

