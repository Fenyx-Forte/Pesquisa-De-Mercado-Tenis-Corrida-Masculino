from loguru import logger

from etl import etl_duckdb
from etl.legado_polars import pipeline_polars
from modulos.uteis import carregar_env, configuracao_loguru, configuracao_polars


def ativar_configuracoes():
    carregar_env.carregar_env()
    configuracao_loguru.configuracao_loguru()
    configuracao_polars.configuracao_polars("../config/polars.json")


def pipeline() -> None:
    logger.info("Inicio pipeline")
    pipeline_polars.pipeline()
    logger.info("Fim pipeline")


def pipeline_duckdb() -> None:
    logger.info("Inicio pipeline")
    etl_duckdb.pipeline()
    logger.info("Fim pipeline")
