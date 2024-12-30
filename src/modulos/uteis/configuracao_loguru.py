"""Módulo de configuração do loguru."""

import sys

from loguru import logger


def configuracao_loguru() -> None:
    """Carrega a configuração do loguru."""
    handlers = [
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
            "sink": "../logs/info.log",
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
    ]

    extra = {"user": "someone"}

    logger.configure(
        handlers=handlers,
        extra=extra,
    )
