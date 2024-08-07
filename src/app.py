from loguru import logger
from modulos.uteis import carregar_env, configuracao_loguru, configuracao_polars


def configurar_loguru() -> None:
    configuracao_loguru.configuracao_loguru()
    logger.info("A")


def configurar_polars() -> None:
    configuracao_polars.configuracao_polars("../config/polars.json")
    logger.info("B")
