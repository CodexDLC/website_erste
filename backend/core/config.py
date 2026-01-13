# backend/core/config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, field_validator
import json

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # === Main ===
    PROJECT_NAME: str = "PinLite"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    DEBUG: bool = False

    # === Database ===
    DATABASE_URL: str 

    # === Storage ===
    UPLOAD_DIR: Path = BASE_DIR / "data" / "uploads"
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5 MB

    # === Logging ===
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

    # === CORS ===
    ALLOWED_ORIGINS: str | list[str] = '["http://localhost"]'
    
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_origins(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [v]  # Если одна строка без JSON
        return v

settings = Settings()

settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.LOG_DIR.mkdir(parents=True, exist_ok=True)
