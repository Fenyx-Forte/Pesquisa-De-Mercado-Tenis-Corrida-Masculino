import duckdb
from etl import duckdb_local
from loguru import logger


def salvar_dados(
    df: duckdb.DuckDBPyRelation,
    query_conexao: str,
    query_insercao: str,
    nome_arquivo: str,
    horario: str,
) -> None:
    logger.info("Iniciando conexao...")

    with duckdb.execute(query_conexao) as conexao:
        logger.info("Conexao criada")
        logger.info("Inserindo dados...")
        conexao.sql(query_insercao)
        logger.info("Dados inseridos")

    duckdb_local.inserir_arquivo(nome_arquivo, horario)

    logger.info("Conexao encerrada")
