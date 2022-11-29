import logging
import logging.config
import sys

LOGGER_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "ntpc_tad_bot.root": {"level": "INFO", "handlers": ["console"]},
        "ntpc_tad_bot.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "propagate": True,
            "qualname": "ntpc_tad_bot.error",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout,
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stderr,
        },
    },
    "formatters": {
        "generic": {
            "format": "%(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
    },
}

logging.config.dictConfig(LOGGER_CONFIG)

logger = logging.getLogger("ntpc_tad_bot.root")
error_logger = logging.getLogger("ntpc_tad_bot.error")
