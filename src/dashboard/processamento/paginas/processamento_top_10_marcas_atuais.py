from duckdb import DuckDBPyConnection
from pandas import DataFrame as pd_DataFrame
from pandas import concat as pd_concat

from dashboard.processamento.queries import queries_top_10_marcas_atuais
from dashboard.uteis import uteis_processamento


def dados_periodo(
    conexao: DuckDBPyConnection,
    data_inicio: str,
    data_fim: str,
    lista_marcas: list[str],
) -> pd_DataFrame:
    periodo = uteis_processamento.retorna_periodo(data_inicio, data_fim)

    query = queries_top_10_marcas_atuais.query_top_10_marcas_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "periodo": periodo,
        "lista_marcas": lista_marcas,
    }

    return conexao.execute(query, parametros).df()


def inicializa_top_10_marcas_atuais(
    conexao: DuckDBPyConnection,
    data_coleta_mais_recente: str,
    data_6_dias_atras: str,
    data_coleta_mais_antiga: str,
    df_hoje: pd_DataFrame,
) -> pd_DataFrame:
    lista_marcas = df_hoje["Marca"].tolist()

    df_ultima_semana = dados_periodo(
        conexao, data_6_dias_atras, data_coleta_mais_recente, lista_marcas
    )

    df_historico = dados_periodo(
        conexao, data_coleta_mais_antiga, data_coleta_mais_recente, lista_marcas
    )

    return pd_concat([df_hoje, df_ultima_semana, df_historico])


def dataframe_a_partir_dados_grafico(
    dados_grafico_atual: dict[str, list[dict]], i: int, qtd_itens: int
):
    return pd_DataFrame(
        {
            "Marca": dados_grafico_atual["data"][i]["x"],
            "Porcentagem": dados_grafico_atual["data"][i]["y"],
            "Periodo": [
                dados_grafico_atual["data"][i]["legendgroup"]
                for n in range(qtd_itens)
            ],
        }
    )


def dados_grafico_atualizado(
    conexao: DuckDBPyConnection,
    dados_grafico_atual: dict[str, list[dict]],
    data_inicio: str,
    data_fim: str,
):
    lista_marcas = dados_grafico_atual["data"][0]["x"]

    qtd_itens = len(lista_marcas)

    df_hoje = dataframe_a_partir_dados_grafico(
        dados_grafico_atual, 0, qtd_itens
    )

    df_novo = dados_periodo(conexao, data_inicio, data_fim, lista_marcas)

    df_historico = dataframe_a_partir_dados_grafico(
        dados_grafico_atual, 2, qtd_itens
    )

    return pd_concat([df_hoje, df_novo, df_historico])
