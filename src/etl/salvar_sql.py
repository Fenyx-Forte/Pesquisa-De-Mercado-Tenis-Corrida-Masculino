from duckdb import DuckDBPyConnection, DuckDBPyRelation
from loguru import logger

from etl import duckdb_local
from modulos.uteis import funcoes_sql


def salvar_dados(
    query_insercao: str,
    df: DuckDBPyRelation,
    conexao: DuckDBPyConnection,
    nome_arquivo: str,
    horario: str,
) -> None:
    logger.info("Iniciando conexao...")
    funcoes_sql.conexao_banco_de_dados_webscraping(conexao)
    logger.info("Conexao criada")

    logger.info("Inserindo dados...")

    conexao.sql(query_insercao)

    logger.info("Dados inseridos")

    conexao.sql("DETACH db;")

    logger.info("Conexao encerrada")

    duckdb_local.inserir_arquivo(nome_arquivo, horario)
