from duckdb import connect
from pandas import DataFrame as pd_DataFrame
from pandas import concat as pd_concat

from modulos.uteis import carregar_env, funcoes_sql, minhas_queries


def inicializacao_dados() -> None:
    global conexao_global
    conexao_global = connect(":memory:")

    carregar_env.carregar_env()

    configurar_duckdb()

    extrair_dados_completos_e_salvar_na_memoria()

    inicializar_dados_mais_recentes()

    inicializar_data_coleta()

    inicializar_dia_coleta_mais_recente()

    inicializar_dia_coleta_mais_antiga()


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


def inicializar_dia_coleta_mais_recente() -> None:
    global dia_coleta_mais_recente

    temp_dia_coleta = data_coleta.split(" - ")[0]

    componentes_dia_coleta = temp_dia_coleta.split("/")

    dia = componentes_dia_coleta[0]
    mes = componentes_dia_coleta[1]
    ano = componentes_dia_coleta[2]

    dia_coleta_mais_recente = f"{ano}-{mes}-{dia}"


def inicializar_dia_coleta_mais_antiga() -> None:
    global dia_coleta_mais_antiga

    query = minhas_queries.dia_coleta_mais_antiga()

    dia_coleta_mais_antiga = conexao_global.sql(query).fetchall()[0][0]


def retorna_data_coleta() -> str:
    return data_coleta


def retorna_dia_coleta_mais_antiga() -> str:
    return dia_coleta_mais_antiga


def retorna_dia_coleta_mais_recente() -> str:
    return dia_coleta_mais_recente


def retorna_dados_dag() -> list[dict]:
    query = minhas_queries.tabela_dag()

    return conexao_global.sql(query).df().to_dict("records")


def retorna_top_10_marcas_dados_mais_recentes() -> pd_DataFrame:
    query = minhas_queries.top_10_marcas_dados_mais_recentes()

    parametros = {"dia_mais_recente": dia_coleta_mais_recente}

    return conexao_global.execute(query, parametros).df()


def formatar_data_pt_br(data: str) -> str:
    componentes = data.split("-")
    dia = componentes[2]
    mes = componentes[1]
    ano = componentes[0]

    return f"{dia}/{mes}/{ano}"


def retorna_top_10_marcas_em_um_periodo(
    data_inicio: str,
    data_fim: str,
    lista_marcas: list[str],
) -> pd_DataFrame:
    query = minhas_queries.top_10_marcas_em_um_periodo()

    periodo = (
        f"{formatar_data_pt_br(data_inicio)} - {formatar_data_pt_br(data_fim)}"
    )

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "lista_marcas": lista_marcas,
        "periodo": periodo,
    }

    return conexao_global.execute(query, parametros).df()


def retorna_dados_grafico_comparacao_top_10(
    dados_grafico_atual: list[dict],
    data_inicio: str,
    data_fim: str,
):
    lista_marcas = dados_grafico_atual["data"][0]["x"]

    qtd_itens_periodo = len(lista_marcas)

    dados_top_10_periodo = retorna_top_10_marcas_em_um_periodo(
        data_inicio, data_fim, lista_marcas
    )

    lista_dataframes = []

    for dados in dados_grafico_atual["data"]:
        dataframe = pd_DataFrame(
            {
                "Marca": dados["x"],
                "Porcentagem": dados["y"],
                "Período": [
                    dados["legendgroup"] for n in range(qtd_itens_periodo)
                ],
            }
        )

        lista_dataframes.append(dataframe)

    lista_dataframes.append(dados_top_10_periodo)

    return pd_concat(lista_dataframes)
