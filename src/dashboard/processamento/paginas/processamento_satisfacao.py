from duckdb import DuckDBPyConnection
from pandas import DataFrame as pd_DataFrame

from dashboard.processamento.queries import queries_satisfacao


def calcular_df_hoje(conexao: DuckDBPyConnection) -> pd_DataFrame:
    query = queries_satisfacao.query_satisfacao_hoje()

    return conexao.sql(query).df()


def calcular_df_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> pd_DataFrame:
    query = queries_satisfacao.query_satisfacao_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return conexao.execute(query, parametros).df()


def dados_num_avaliacoes(df: pd_DataFrame) -> pd_DataFrame:
    return df.loc[
        df["tipo_linha"] == "num_avaliacoes",
        ["marca", "nota_avaliacao", "num_avaliacoes"],
    ].sort_values(
        by=["num_avaliacoes", "nota_avaliacao", "marca"],
        ascending=[False, False, True],
    )


def dados_avaliacao(df: pd_DataFrame) -> pd_DataFrame:
    return df.loc[
        df["tipo_linha"] == "avaliacao",
        ["marca", "nota_avaliacao", "num_avaliacoes"],
    ].sort_values(
        by=["nota_avaliacao", "num_avaliacoes", "marca"],
        ascending=[False, False, True],
    )


def dados_hoje(conexao: DuckDBPyConnection) -> dict[str, list[dict]]:
    df_hoje = calcular_df_hoje(conexao)

    df_num_avaliacao = dados_num_avaliacoes(df_hoje)

    df_avaliacao = dados_avaliacao(df_hoje)

    return {
        "dados_mais_20_avaliacoes": df_num_avaliacao.to_dict("records"),
        "dados_nota_superior_4": df_avaliacao.to_dict("records"),
    }


def dados_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> dict[str, list[dict]]:
    df_periodo = calcular_df_periodo(conexao, data_inicio, data_fim)

    df_num_avaliacao = dados_num_avaliacoes(df_periodo)

    df_avaliacao = dados_avaliacao(df_periodo)

    return {
        "dados_mais_20_avaliacoes": df_num_avaliacao.to_dict("records"),
        "dados_nota_superior_4": df_avaliacao.to_dict("records"),
    }
