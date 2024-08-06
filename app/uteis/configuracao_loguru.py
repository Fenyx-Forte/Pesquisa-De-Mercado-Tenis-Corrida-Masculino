import sys


def configuracao_loguru() -> dict:
    configuracao = {
        "handlers": [
            {
                "sink": sys.stderr,
                "level": "INFO",
                "format": (
                    "<green>{time:DD-MM-YYYY HH:mm:ss}</green> | "
                    "<level>{level}</level> | "
                    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                    "{message}"
                ),
                "backtrace": False,
                "diagnose": False,
                "enqueue": True,
            },
            {
                "sink": "logs/info.log",
                "rotation": "1 MB",
                "delay": True,
                "level": "INFO",
                "format": (
                    "<green>{time:DD-MM-YYYY HH:mm:ss}</green> | "
                    "<level>{level}</level> | "
                    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                    "{message}"
                ),
                "backtrace": False,
                "diagnose": False,
                "enqueue": True,
            },
        ],
        "extra": {"user": "someone"},
    }

    return configuracao
