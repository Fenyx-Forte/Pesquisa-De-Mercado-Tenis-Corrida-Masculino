import duckdb
from etl import duckdb_local
from loguru import logger
from modulos.uteis import ler_sql


def salvar_dados(
    df: duckdb.DuckDBPyRelation,
    query_insercao: str,
    nome_arquivo: str,
    horario: str,
) -> None:
    logger.info("Iniciando conexao...")

    with ler_sql.conexao_banco_de_dados() as conexao:
        logger.info("Conexao criada")
        logger.info("Inserindo dados...")
        conexao.sql(query_insercao)
        logger.info("Dados inseridos")

    logger.info("Conexao encerrada")

    duckdb_local.inserir_arquivo(nome_arquivo, horario)
