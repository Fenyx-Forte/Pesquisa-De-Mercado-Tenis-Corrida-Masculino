from duckdb import DuckDBPyConnection, connect

from dashboard.processamento import tabelas_sql
from modulos.uteis import carregar_env, funcoes_sql


def query_cabecalho_data_coleta() -> str:
    query = """
    SELECT
        CONCAT(
            STRFTIME(data_coleta, '%d/%m/%Y')
            , ' - '
            , horario_coleta::VARCHAR
        ) AS coluna_data_coleta
    FROM
        dados_mais_recentes
    LIMIT
        1;
    """

    return query


def query_data_coleta_mais_recente() -> str:
    query = """
    SELECT
        STRFTIME(data_coleta, '%Y-%m-%d') as data_coleta
    FROM
        dados_mais_recentes
    LIMIT
        1;
    """

    return query


def query_data_coleta_mais_antiga() -> str:
    query = """
    SELECT
        STRFTIME(data_coleta, '%Y-%m-%d') as data_coleta
    FROM
        dados_completos
    ORDER BY
        data_coleta ASC
    LIMIT
        1;
    """

    return query


def inicializar_variaveis_ambiente() -> None:
    carregar_env.carregar_env()


def inicializar_conexao_duckdb() -> DuckDBPyConnection:
    return connect(":memory:")


def configurar_duckdb(conexao: DuckDBPyConnection) -> None:
    configuracao = """
    SET threads TO 1;
    SET memory_limit = '200MB';
    """

    conexao.sql(configuracao)


def inicializar_tabela_dados_completos(conexao: DuckDBPyConnection) -> None:
    query = tabelas_sql.tabela_dados_completos()

    funcoes_sql.conexao_banco_de_dados_dashboard(conexao)

    conexao.sql(query)


def inicializar_tabela_dados_mais_recentes(conexao: DuckDBPyConnection) -> None:
    query = tabelas_sql.tabela_dados_mais_recentes()

    conexao.sql(query)


def inicializar_cabecalho_data_coleta(conexao: DuckDBPyConnection) -> str:
    query = query_cabecalho_data_coleta()

    cabecalho_data_coleta = conexao.sql(query).fetchall()[0][0]

    return cabecalho_data_coleta


def inicializar_data_coleta_mais_recente(conexao: DuckDBPyConnection) -> str:
    query = query_data_coleta_mais_recente()

    data_coleta_mais_recente = conexao.sql(query).fetchall()[0][0]

    return data_coleta_mais_recente


def inicializar_data_coleta_mais_antiga(conexao: DuckDBPyConnection) -> str:
    query = query_data_coleta_mais_antiga()

    data_coleta_mais_antiga = conexao.sql(query).fetchall()[0][0]

    return data_coleta_mais_antiga
