"""Módulo responsável por salvar os dados tratados, resultados do ETL, no banco de dados na nuvem."""

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
    """Salva os dados tratados, resultados do ETL, no banco de dados na nuvem.

    Além disso, salva o nome do arquivo e o horário em que os dados foram extraídos no banco de dados local.

    Args:
        query_insercao (str): Consulta SQL para inserir os dados no banco de dados na nuvem.
        df (DuckDBPyRelation): Dados tratados, resultados do ETL.
        conexao (DuckDBPyConnection): Conexão com o banco de dados na nuvem.
        nome_arquivo (str): Nome do arquivo que será salvo no banco de dados local.
        horario (str): Horário em que o arquivo será salvo no banco de dados local.
    """
    logger.info("Iniciando conexao...")
    funcoes_sql.conexao_banco_de_dados_webscraping(conexao)
    logger.info("Conexao criada")

    logger.info("Inserindo dados...")

    conexao.sql(query_insercao)

    logger.info("Dados inseridos")

    conexao.sql("DETACH db;")

    logger.info("Conexao encerrada")

    duckdb_local.inserir_arquivo(nome_arquivo, horario)
