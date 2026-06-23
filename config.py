from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "Bella Tavola API"
    app_version: str = "1.0.0"
    debug: bool = False
    max_mesas: int = 20
    max_pessoas_por_mesa: int = 10
    database_path: str = "data/bella_tavola.db"


settings = Settings()
