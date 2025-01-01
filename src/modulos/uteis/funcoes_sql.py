"""Módulo de funções para manipulação de SQL via DuckDB."""

from os import getenv
from pathlib import Path

from duckdb import DuckDBPyConnection, DuckDBPyRelation, connect
from polars import DataFrame


class ConexaoError(Exception):
    """Erro ao tentar estabelecer uma conexão com o banco de dados."""

    def __init__(
        self,
        message: str = "Conexão com o banco de dados falhou.",
    ) -> None:
        """Inicialização da classe.

        Args:
            message (str): Mensagem de erro.
        """
        self.message = message
        super().__init__(self.message)


def ler_conteudo_query(caminho_query: str) -> str:
    """Lê o conteúdo de um arquivo de query.

    Args:
        caminho_query (str): Caminho para o arquivo de query.

    Returns:
        str: Conteúdo do arquivo de query.
    """
    query: str
    with Path(caminho_query).open() as file:
        query = file.read()

    return query


def string_conexao_banco_de_dados_webscraping() -> str:
    """Cria a string de conexão com o banco de dados do webscraping.

    Returns:
        str: String de conexão com o banco de dados do webscraping.
    """
    return f"""
        ATTACH '{getenv("DATABASE_URL_WEBSCRAPING")}' AS db (TYPE POSTGRES);
    """


def string_conexao_banco_de_dados_dashboard() -> str:
    """Cria a string de conexão com o banco de dados do dashboard.

    Returns:
        str: String de conexão com o banco de dados do dashboard.
    """
    return f"""
        ATTACH '{getenv("DATABASE_URL_DASHBOARD")}' AS db (TYPE POSTGRES, READ_ONLY);
    """


def conexao_banco_de_dados_webscraping(conexao: DuckDBPyConnection) -> None:
    """Tenta estabelecer uma conexão com o banco de dados do webscraping.

    Args:
        conexao (DuckDBPyConnection): Conexão com o banco de dados do webscraping.

    Raises:
        ConexaoError: Falha na conexão com o banco de dados.
    """
    try:
        conexao.sql(string_conexao_banco_de_dados_webscraping())
    except Exception:
        raise ConexaoError from None


def conexao_banco_de_dados_dashboard(conexao: DuckDBPyConnection) -> None:
    """Tenta estabelecer uma conexão com o banco de dados do dashboard.

    Args:
        conexao (DuckDBPyConnection): Conexão com o banco de dados do dashboard.

    Raises:
        ConexaoError: Falha na conexão com o banco de dados.
    """
    try:
        conexao.sql(string_conexao_banco_de_dados_dashboard())
    except Exception:
        raise ConexaoError from None


def query_pl_para_pl(query: str, df: DataFrame) -> DataFrame:
    """Realiza uma query em um dataframe do Polars e retorna o resultado em outro dataframe do Polars.

    Args:
        query (str): Query a ser executada no dataframe do Polars
        df (DataFrame): Dataframe do Polars no qual a query será executada

    Returns:
        DataFrame: Resultado da query executada no dataframe do Polars
    """
    with connect(":memory:") as conexao:
        return conexao.sql(query).pl()


def query_pl_para_pl_com_parametro(
    query: str,
    parametros: dict,
    df: DataFrame,
) -> DataFrame:
    """Realiza uma query em um dataframe do Polar utilizando paramêtros e retorna o resultado em outro dataframe do Polars.

    Args:
        query (str): Query a ser executada no dataframe do Polars
        parametros (dict): Dicionário contendo os parâmetros a serem passados para a query
        df (DataFrame): Dataframe do Polars onde a query será executada

    Returns:
        DataFrame: Resultado da query em formato de dataframe do Polars
    """
    with connect(":memory:") as conexao:
        return conexao.execute(query, parametros).pl()


def query_duckbdb_para_pl(
    query: str,
    df: DuckDBPyRelation,
    conexao: DuckDBPyConnection,
) -> DataFrame:
    """Realiza uma query em um dataframe do DuckDB e retorna o resultado em outro dataframe do Polars.

    Args:
        query (str): Query a ser executada no dataframe do DuckDB
        df (DuckDBPyRelation): Dataframe do DuckDB no qual a query será executada
        conexao (DuckDBPyConnection): Conexão com o banco de dados do DuckDB

    Returns:
        DataFrame: Resultado da query em formato de dataframe do Polars
    """
    return conexao.sql(query).pl()


def query_duckdb_para_duckdb(
    query: str,
    df: DuckDBPyRelation,
    conexao: DuckDBPyConnection,
) -> DuckDBPyRelation:
    """Realiza uma query em um dataframe do DuckDB e retorna o resultado em outro dataframe do Duckdb.

    Args:
        query (str): Query a ser executada no dataframe do DuckDB
        df (DuckDBPyRelation): Dataframe do DuckDB no qual a query será executada
        conexao (DuckDBPyConnection): Conexão com o banco de dados do DuckDB

    Returns:
        DuckDBPyRelation: Resultado da query em formato de dataframe do DuckDB
    """
    return conexao.sql(query)
