from dashboard import dash_dash
from modulos.pipelines import pipeline_mercado_livre
from modulos.uteis import carregar_env, configuracao_loguru, configuracao_polars


def configurar_loguru() -> None:
    configuracao_loguru.configuracao_loguru()


def configurar_polars() -> None:
    configuracao_polars.configuracao_polars("../config/polars.json")


def pipeline():
    caminho_json = "../dados/nao_processados/mercado_livre.json"
    caminho_parquet = "../dados/processados/mercado_livre.parquet"
    pipeline_mercado_livre.pipeline(caminho_json, caminho_parquet)


def dash_dashboard():
    dash_dash.dashboard()
