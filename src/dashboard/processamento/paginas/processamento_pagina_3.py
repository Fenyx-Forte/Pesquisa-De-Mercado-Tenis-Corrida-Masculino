from duckdb import DuckDBPyConnection
from pandas import DataFrame as pd_DataFrame


def verifica_se_datas_sao_validas(data_inicio: str, data_fim: str) -> bool:
    if (data_inicio is None) or (data_fim is None):
        return False

    return True


def query_top_10_marcas_historico() -> str:
    query = """
    SELECT
        marca AS Marca
        , porcentagem AS Porcentagem
        , periodo AS Periodo
    FROM
        top_10_marcas_historico($periodo)
    WHERE
        Marca <> 'GENERICA'
    ORDER BY
        Porcentagem DESC
    LIMIT
        10;
    """

    return query


def query_top_10_marcas_periodo() -> str:
    query = """
    SELECT
        marca AS Marca
        , porcentagem AS Porcentagem
        , periodo AS Periodo
    FROM
        top_10_marcas_periodo($periodo, $data_inicio, $data_fim)
    WHERE
        Marca <> 'GENERICA'
    ORDER BY
        Porcentagem DESC
    LIMIT
        10;
    """

    return query


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
    query = query_top_10_marcas_historico()

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

    query = query_top_10_marcas_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "periodo": periodo,
    }

    return conexao.execute(query, parametros).df()
