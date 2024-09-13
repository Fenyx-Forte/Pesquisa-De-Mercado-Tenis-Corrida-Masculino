from duckdb import DuckDBPyConnection
from pandas import DataFrame as pd_DataFrame
from plotly.graph_objects import Figure

from dashboard.processamento.queries import pagina_3_queries


def verifica_se_datas_sao_validas(data_inicio: str, data_fim: str) -> bool:
    if (data_inicio is None) or (data_fim is None):
        return False

    return True


def verifica_se_qtd_maxima_de_graficos_ja_foi_adicionada(
    grafico_2: Figure, grafico_3: Figure
) -> bool:
    if (grafico_2 is None) or (grafico_3 is None):
        return False

    return True


def verifica_se_periodo_ja_foi_adicionado(
    data_inicio: str, data_fim: str, grafico_1: Figure, grafico_2: Figure
) -> bool:
    data_inicio_formatada = formatar_data_pt_br(data_inicio)
    data_fim_formatada = formatar_data_pt_br(data_fim)

    periodo = f"{data_inicio_formatada} - {data_fim_formatada}"

    periodos = []

    for grafico in [grafico_1, grafico_2]:
        if grafico is not None:
            periodos.append(grafico["data"][0]["legendgroup"])

    return periodo in periodos


def formatar_data_pt_br(data: str) -> str:
    # "data" esta no formato YYYY/MM/DD
    componentes = data.split("-")
    dia = componentes[2]
    mes = componentes[1]
    ano = componentes[0]

    return f"{dia}/{mes}/{ano}"


def inicializa_top_10_marcas_historico(
    conexao: DuckDBPyConnection,
    data_inicio: str,
    data_fim: str,
) -> pd_DataFrame:
    query = pagina_3_queries.query_top_10_marcas_historico()

    data_inicio_formatada = formatar_data_pt_br(data_inicio)
    data_fim_formatada = formatar_data_pt_br(data_fim)

    periodo = f"{data_inicio_formatada} - {data_fim_formatada}"
    parametros = {"periodo": periodo}

    return conexao.execute(query, parametros).df()


def top_10_marcas_periodo(
    conexao: DuckDBPyConnection,
    data_inicio: str,
    data_fim: str,
) -> pd_DataFrame:
    data_inicio_formatada = formatar_data_pt_br(data_inicio)
    data_fim_formatada = formatar_data_pt_br(data_fim)

    periodo = f"{data_inicio_formatada} - {data_fim_formatada}"

    query = pagina_3_queries.query_top_10_marcas_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "periodo": periodo,
    }

    return conexao.execute(query, parametros).df()
