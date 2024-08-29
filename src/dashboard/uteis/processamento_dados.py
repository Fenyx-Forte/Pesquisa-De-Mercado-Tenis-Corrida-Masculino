from duckdb import connect

from modulos.uteis import carregar_env, funcoes_sql, meu_tempo, minhas_queries


def inicializacao() -> None:
    global conexao_global
    conexao_global = connect(":memory:")

    carregar_env.carregar_env()

    extrair_dados_mais_recentes_e_salvar_dados_na_memoria()

    inicializar_data_coleta()


def extrair_dados_mais_recentes_e_salvar_dados_na_memoria() -> None:
    query = minhas_queries.dados_mais_recentes_do_banco_de_dados()

    funcoes_sql.conexao_banco_de_dados_apenas_leitura(conexao_global)

    conexao_global.sql(query)


def inicializar_data_coleta() -> None:
    global data_coleta

    query = minhas_queries.data_coleta_mais_recente()

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
