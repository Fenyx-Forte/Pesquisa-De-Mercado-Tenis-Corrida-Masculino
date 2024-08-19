from etl import etl_duckdb, pipeline_mercado_livre
from loguru import logger
from modulos.uteis import carregar_env, configuracao_loguru, configuracao_polars


def ativar_configuracoes():
    carregar_env.carregar_env()
    configuracao_loguru.configuracao_loguru()
    configuracao_polars.configuracao_polars("../config/polars.json")


def pipeline() -> None:
    logger.info("Inicio pipeline")
    pipeline_mercado_livre.pipeline()
    logger.info("Fim pipeline")


def pipeline_duckdb() -> None:
    logger.info("Inicio pipeline")
    etl_duckdb.pipeline()
    logger.info("Fim pipeline")
