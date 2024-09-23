from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    TG_TOKEN: str
    DB_CLUSTER: str
    DB_URL: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()