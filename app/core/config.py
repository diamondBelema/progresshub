from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    appwrite_endpoint: str = ""
    appwrite_project_id: str = ""
    appwrite_api_key: str = ""
    openrouter_api_key: str = ""
    secret_key: str = ""
    appwrite_database_id: str = ""
    appwrite_profiles_collection_id: str = ""
    appwrite_sessions_collection_id: str = ""
    appwrite_challenges_collection_id: str = ""
    appwrite_goals_collection_id: str = "goals"
    appwrite_checkins_collection_id: str = "checkins"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
