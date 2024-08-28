from duckdb import DuckDBPyConnection, DuckDBPyRelation
from loguru import logger

from modulos.uteis import funcoes_sql


def salvar_dados(
    query_insercao: str,
    df: DuckDBPyRelation,
    conexao: DuckDBPyConnection,
) -> None:
    logger.info("Iniciando conexao...")
    funcoes_sql.conexao_banco_de_dados(conexao)
    logger.info("Conexao criada")

    logger.info("Inserindo dados...")
    conexao.sql(query_insercao)
    logger.info("Dados inseridos")
