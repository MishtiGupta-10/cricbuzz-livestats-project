import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "CricInsight")
    app_version: str = os.getenv("APP_VERSION", "0.1.0")
    environment: str = os.getenv("APP_ENV", "development")
    api_prefix: str = os.getenv("API_PREFIX", "/api/v1")
    rapidapi_key: str | None = os.getenv("RAPIDAPI_KEY")
    cricbuzz_base_url: str = os.getenv(
        "CRICBUZZ_BASE_URL",
        "https://cricbuzz-cricket.p.rapidapi.com",
    )
    cricbuzz_host: str = os.getenv(
        "CRICBUZZ_HOST",
        "cricbuzz-cricket.p.rapidapi.com",
    )
    request_timeout_seconds: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", "60"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    database_url: str = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:root@localhost:3306/cricinsight")
    sync_interval_minutes: int = int(os.getenv("SYNC_INTERVAL_MINUTES", "5"))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
