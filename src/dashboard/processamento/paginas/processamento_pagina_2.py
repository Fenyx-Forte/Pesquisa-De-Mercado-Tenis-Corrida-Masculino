from duckdb import DuckDBPyConnection
from pandas import DataFrame as pd_DataFrame
from pandas import concat as pd_concat


def query_top_10_marcas_atual() -> str:
    query = """
    WITH marcas_dados_mais_recentes as (
        SELECT
            dmr.marca as Marca
            , (
                COUNT(marca) * 100.0 / (SUM(COUNT(*)) OVER())
            ) as Porcentagem
            , $data_mais_recente as Período
        FROM
            dados_mais_recentes as dmr
        GROUP BY
            dmr.marca
    )
    SELECT
        *
    FROM
        marcas_dados_mais_recentes
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
    WITH marcas_em_um_periodo AS (
        SELECT
            dc.marca as Marca
            , (
                COUNT(marca) * 100.0 / (SUM(COUNT(*)) OVER())
            ) as Porcentagem
            , $periodo as Período
        FROM
            dados_completos as dc
        WHERE
            dc.data_coleta BETWEEN $data_inicio AND $data_fim
        GROUP BY
            dc.marca
    )
    SELECT
        *
    FROM
        marcas_em_um_periodo
    WHERE
        Marca IN (SELECT UNNEST ($lista_marcas))
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


def inicializa_top_10_marcas_atual(
    conexao: DuckDBPyConnection, data_coleta_mais_recente: str
) -> pd_DataFrame:
    query = query_top_10_marcas_atual()

    parametros = {"data_mais_recente": data_coleta_mais_recente}

    return conexao.execute(query, parametros).df()


def top_10_marcas_periodo(
    conexao: DuckDBPyConnection,
    data_inicio: str,
    data_fim: str,
    lista_marcas: list[str],
) -> pd_DataFrame:
    data_inicio_formatada = formatar_data_pt_br(data_inicio)
    data_fim_formatada = formatar_data_pt_br(data_fim)

    periodo = f"{data_inicio_formatada} - {data_fim_formatada}"

    query = query_top_10_marcas_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "lista_marcas": lista_marcas,
        "periodo": periodo,
    }

    return conexao.execute(query, parametros).df()


def dados_grafico_comparacao_top_10(
    conexao: DuckDBPyConnection,
    dados_grafico_atual: list[dict],
    data_inicio: str,
    data_fim: str,
) -> pd_DataFrame:
    lista_marcas = dados_grafico_atual["data"][0]["x"]

    qtd_itens_periodo = len(lista_marcas)

    dados_top_10_periodo = top_10_marcas_periodo(
        conexao, data_inicio, data_fim, lista_marcas
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
