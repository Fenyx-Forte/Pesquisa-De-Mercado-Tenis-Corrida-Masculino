from etl import pipeline_mercado_livre
from modulos.uteis import carregar_env, configuracao_loguru, configuracao_polars


def configurar_loguru() -> None:
    configuracao_loguru.configuracao_loguru()


def configurar_polars() -> None:
    configuracao_polars.configuracao_polars("../config/polars.json")


def pipeline() -> None:
    pipeline_mercado_livre.pipeline()
