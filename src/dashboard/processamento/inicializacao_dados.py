from duckdb import DuckDBPyConnection, connect
from pandas import DataFrame as pd_DataFrame

from dashboard.processamento import macros_sql, tabelas_sql
from modulos.uteis import carregar_env, funcoes_sql


def formatar_data_pt_br(data: str) -> str:
    # "data" esta no formato YYYY-MM-DD
    componentes = data.split("-")
    dia = componentes[2]
    mes = componentes[1]
    ano = componentes[0]

    return f"{dia}/{mes}/{ano}"


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


def query_data_6_dias_atras() -> str:
    query = """
    SELECT
        STRFTIME(data_coleta - INTERVAL 6 DAY, '%Y-%m-%d') as data_6_dias_atras
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


def query_top_10_marcas_hoje() -> str:
    query = """
    WITH marcas_agrupadas AS (
        SELECT
            dmr.marca AS marca
            , (
                COUNT(marca) * 100.0 / (SUM(COUNT(*)) OVER())
            ) AS porcentagem
        FROM
            dados_mais_recentes AS dmr
        GROUP BY
            dmr.marca
    )
    SELECT
        marca AS Marca
        , porcentagem AS Porcentagem
        , $periodo AS Periodo
    FROM
        marcas_agrupadas
    WHERE
        Marca <> 'GENERICA'
    ORDER BY
        porcentagem DESC
    LIMIT
        10;
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


def inicializar_macro_dados_completos_por_periodo(
    conexao: DuckDBPyConnection,
) -> None:
    query = macros_sql.macro_dados_completos_por_periodo()

    conexao.sql(query)


def inicializar_macro_top_10_marcas_periodo(
    conexao: DuckDBPyConnection,
) -> None:
    query = macros_sql.macro_top_10_marcas_periodo()

    conexao.sql(query)


def inicializar_macro_preco_medio_periodo(conexao: DuckDBPyConnection) -> None:
    query = macros_sql.macro_preco_medio_periodo()

    conexao.sql(query)


def inicializar_macro_faixa_preco_periodo(conexao: DuckDBPyConnection) -> None:
    query = macros_sql.macro_faixa_preco_periodo()

    conexao.sql(query)


def inicializar_cabecalho_data_coleta(conexao: DuckDBPyConnection) -> str:
    query = query_cabecalho_data_coleta()

    cabecalho_data_coleta = conexao.sql(query).fetchall()[0][0]

    return cabecalho_data_coleta


def inicializar_data_coleta_mais_recente(conexao: DuckDBPyConnection) -> str:
    query = query_data_coleta_mais_recente()

    data_coleta_mais_recente = conexao.sql(query).fetchall()[0][0]

    return data_coleta_mais_recente


def inicializar_data_6_dias_atras(conexao: DuckDBPyConnection) -> str:
    query = query_data_6_dias_atras()

    data_6_dias_atras = conexao.sql(query).fetchall()[0][0]

    return data_6_dias_atras


def inicializar_data_coleta_mais_antiga(conexao: DuckDBPyConnection) -> str:
    query = query_data_coleta_mais_antiga()

    data_coleta_mais_antiga = conexao.sql(query).fetchall()[0][0]

    return data_coleta_mais_antiga


def inicializar_periodo_hoje(data_coleta_mais_recente: str) -> str:
    data_hoje = formatar_data_pt_br(data_coleta_mais_recente)

    return f"{data_hoje} - {data_hoje}"


def inicializar_periodo_ultima_semana(
    data_6_dias_atras: str, data_coleta_mais_recente: str
) -> str:
    data_6_dias_atras_formatada = formatar_data_pt_br(data_6_dias_atras)

    data_hoje = formatar_data_pt_br(data_coleta_mais_recente)

    return f"{data_6_dias_atras_formatada} - {data_hoje}"


def inicializar_periodo_historico(
    data_coleta_mais_antiga: str, data_coleta_mais_recente: str
) -> str:
    data_mais_antiga = formatar_data_pt_br(data_coleta_mais_antiga)

    data_mais_recente = formatar_data_pt_br(data_coleta_mais_recente)

    return f"{data_mais_antiga} - {data_mais_recente}"


def inicializar_df_top_10_marcas_hoje(
    conexao: DuckDBPyConnection, data_coleta_mais_recente: str
) -> pd_DataFrame:
    query = query_top_10_marcas_hoje()

    data_hoje = formatar_data_pt_br(data_coleta_mais_recente)

    periodo = f"{data_hoje} - {data_hoje}"

    parametros = {
        "periodo": periodo,
    }

    return conexao.execute(query, parametros).df()
