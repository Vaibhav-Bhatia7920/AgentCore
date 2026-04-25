from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from functools import lru_cache

class Settings(BaseSettings):
    db_url : str = "postgresql://user:password@localhost:5432/agent_db"
    app_name : str  = "ACore"
    api_key : SecretStr | None = None
    app_env : str = "dev"

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    settings = Settings()
    return settings

settings = get_settings()