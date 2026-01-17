import logging
import sys
from types import FrameType

from loguru import logger

from .config import settings


class InterceptHandler(logging.Handler):
    """
    Intercepts standard logging messages and redirects them to Loguru.
    """

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame: FrameType | None = logging.currentframe()
        depth = 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def setup_loguru() -> None:
    """
    Configures Loguru logger.
    Sets up sinks for console, debug file, and error JSON file.
    Intercepts standard library logging.
    """
    logger.remove()

    # --- Console Sink ---
    logger.add(
        sink=sys.stdout,
        level=settings.LOG_LEVEL_CONSOLE.upper(),
        colorize=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
    )

    # --- File Sink (Debug) ---
    logger.add(
        sink=str(settings.log_file_debug),
        level=settings.LOG_LEVEL_FILE.upper(),
        rotation=settings.LOG_ROTATION,
        compression="zip",
        format="{time} | {level: <8} | {name}:{function}:{line} - {message}",
    )

    # --- File Sink (Errors JSON) ---
    logger.add(
        sink=str(settings.log_file_errors),
        level="ERROR",
        serialize=True,
        rotation=settings.LOG_ROTATION,
        compression="zip",
    )

    # --- Intercept Standard Logging ---
    logging.basicConfig(handlers=[InterceptHandler()], level=0)

    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.error").handlers = [InterceptHandler()]

    # Third-party loggers configuration
    logging.getLogger("aiogram").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("aiosqlite").setLevel(logging.INFO)

    logger.info("Logger configured successfully")
