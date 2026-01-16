import logging.config
import os

from shop_app.core.config import ENVIRONMENT, LOG_DIR

os.makedirs(LOG_DIR, exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_id": {
            "()": "shop_app.logging.filters.RequestIdFilter",
        }
    },
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.json.JsonFormatter",
            "format": ("%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s"),
        }
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "filters": ["request_id"],
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": os.path.join(LOG_DIR, "shop_app.log"),
            "maxBytes": 5 * 1024 * 1024,  # 5 MB
            "backupCount": 3,
            "encoding": "utf-8",
            "filters": ["request_id"],
        },
        "access_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": os.path.join(LOG_DIR, "access_shop_app.log"),
            "maxBytes": 5 * 1024 * 1024,  # 5 MB
            "backupCount": 3,
            "encoding": "utf-8",
            "filters": ["request_id"],
        },
    },
    "loggers": {
        "": {
            "handlers": ["default", "file"],
            "level": "INFO" if ENVIRONMENT == "prod" else "DEBUG",
        },
        "access": {
            "handlers": ["default", "access_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


def setup_logging() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
