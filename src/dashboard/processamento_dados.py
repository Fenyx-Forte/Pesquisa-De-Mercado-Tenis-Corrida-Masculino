from duckdb import connect
from polars import DataFrame

from modulos.uteis import carregar_env, ler_sql, minhas_queries


def inicializacao() -> None:
    global conexao_global

    conexao_global = connect(":memory:conexao_global")

    carregar_env.carregar_env()

    df_geral = extrair_dados_mais_recentes()

    salvar_dados_na_memoria_duckdb(df_geral)

    inicializar_data_coleta()


def extrair_dados_mais_recentes() -> DataFrame:
    query = minhas_queries.dados_mais_recentes_do_banco_de_dados()

    return ler_sql.query_banco_de_dados_apenas_leitura(query)


def salvar_dados_na_memoria_duckdb(df_geral: DataFrame) -> None:
    query = """
    CREATE TABLE
        minha_tabela AS
    SELECT
        *
    FROM
        df_geral
    """

    conexao_global.sql(query)


def inicializar_data_coleta() -> None:
    global data_coleta

    query = """
    SELECT
        CONCAT(
            STRFTIME(_data_coleta, '%d/%m/%Y')
            , ' - '
            , _horario_coleta::VARCHAR
        ) AS coluna_data_coleta
    FROM
        minha_tabela
    LIMIT
        1;
    """

    data_coleta = conexao_global.sql(query).fetchall()[0][0]


def recuperar_data_coleta() -> str:
    return data_coleta


def recuperar_dados_dag() -> list[dict]:
    query = """
    SELECT
        marca
        , produto
        , preco_atual
        , promocao
        , percentual_promocao
    FROM
        minha_tabela;
    """

    return conexao_global.sql(query).df().to_dict("records")
