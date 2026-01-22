import json
from pathlib import Path
from typing import Any

from pydantic import computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """
    Application Configuration.
    Loads settings from environment variables (.env file).
    """

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Main ---
    PROJECT_NAME: str = "PinLite"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    DEBUG: bool = False
    
    # Domain settings for generating absolute URLs
    SITE_URL: str = "http://localhost:8000"



    # --- Security ---
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # --- Database ---
    DATABASE_URL: str
    AUTO_MIGRATE: bool = True

    # --- Storage ---
    UPLOAD_DIR: Path = BASE_DIR / "data" / "uploads"
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5 MB

    # --- Logging ---
    LOG_LEVEL_CONSOLE: str = "INFO"
    LOG_LEVEL_FILE: str = "DEBUG"
    LOG_ROTATION: str = "10 MB"
    LOG_DIR: Path = BASE_DIR / "data" / "logs"

    @computed_field
    def log_file_debug(self) -> Path:
        return self.LOG_DIR / "debug.log"

    @computed_field
    def log_file_errors(self) -> Path:
        return self.LOG_DIR / "errors.json"

    # --- CORS ---
    ALLOWED_ORIGINS: str | list[str] = '["*"]'

    @field_validator("ALLOWED_ORIGINS", mode="before")
    def parse_origins(cls, v: Any) -> Any:
        """
        Parses a JSON string of origins into a list.
        """
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [v]
        return v
    
    @field_validator("SITE_URL")
    def validate_site_url(cls, v: str) -> str:
        """
        Ensure SITE_URL does not end with a slash.
        """
        return v.rstrip("/")


settings = Settings()

# Ensure critical directories exist
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.LOG_DIR.mkdir(parents=True, exist_ok=True)
