from duckdb import connect

from modulos.uteis import carregar_env, funcoes_sql, minhas_queries


def inicializacao_dados() -> None:
    global conexao_global
    conexao_global = connect(":memory:")

    carregar_env.carregar_env()

    configurar_duckdb()

    extrair_dados_completos_e_salvar_na_memoria()

    inicializar_dados_mais_recentes()

    inicializar_data_coleta()


def configurar_duckdb() -> None:
    configuracao = """
    SET threads TO 1;
    SET memory_limit = '200MB';
    """

    conexao_global.sql(configuracao)


def extrair_dados_completos_e_salvar_na_memoria() -> None:
    query = minhas_queries.dados_completos_do_banco_de_dados()

    funcoes_sql.conexao_banco_de_dados_dashboard(conexao_global)

    conexao_global.sql(query)


def inicializar_dados_mais_recentes() -> None:
    query = minhas_queries.dados_mais_recentes()

    conexao_global.sql(query)


def inicializar_data_coleta() -> None:
    global data_coleta

    query = minhas_queries.data_coleta_mais_recente()

    data_coleta = conexao_global.sql(query).fetchall()[0][0]


def recuperar_data_coleta() -> str:
    return data_coleta


def recuperar_dados_dag() -> list[dict]:
    query = minhas_queries.tabela_dag()

    return conexao_global.sql(query).df().to_dict("records")
