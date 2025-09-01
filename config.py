from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    environment: str
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_database: str

settings = Settings()