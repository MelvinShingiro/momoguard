from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "MomoGuard"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    model_version: str = "untrained-placeholder"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
