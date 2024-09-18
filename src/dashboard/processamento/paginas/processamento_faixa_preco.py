from duckdb import DuckDBPyConnection
from pandas import DataFrame as pd_DataFrame

from dashboard.processamento.queries import queries_faixa_preco


def calcular_df_hoje(conexao: DuckDBPyConnection) -> pd_DataFrame:
    query = queries_faixa_preco.query_faixas_preco_hoje()

    return conexao.sql(query).df()


def calcular_df_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> pd_DataFrame:
    query = queries_faixa_preco.query_faixas_preco_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return conexao.execute(query, parametros).df()


def dados_abaixo_de_200(df: pd_DataFrame) -> pd_DataFrame:
    return df.loc[df["faixa_preco"] == "200"].sort_values(
        by=["num_produtos", "marca"],
        ascending=[False, True],
    )


def dados_entre_200_e_400_(df: pd_DataFrame) -> pd_DataFrame:
    return df.loc[df["faixa_preco"] == "200_400"].sort_values(
        by=["num_produtos", "marca"],
        ascending=[False, True],
    )


def dados_acima_de_400_(df: pd_DataFrame) -> pd_DataFrame:
    return df.loc[df["faixa_preco"] == "400"].sort_values(
        by=["num_produtos", "marca"],
        ascending=[False, True],
    )


def dados_hoje(conexao: DuckDBPyConnection) -> dict[str, list[dict]]:
    df_hoje = calcular_df_hoje(conexao)

    df_abaixo_de_200 = dados_abaixo_de_200(df_hoje)

    df_entre_200_e_400 = dados_entre_200_e_400_(df_hoje)

    df_acima_de_400 = dados_acima_de_400_(df_hoje)

    return {
        "dados_abaixo_de_200": df_abaixo_de_200.to_dict("records"),
        "dados_entre_200_e_400": df_entre_200_e_400.to_dict("records"),
        "dados_acima_de_400": df_acima_de_400.to_dict("records"),
    }


def dados_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> dict[str, list[dict]]:
    df_periodo = calcular_df_periodo(conexao, data_inicio, data_fim)

    df_abaixo_de_200 = dados_abaixo_de_200(df_periodo)

    df_entre_200_e_400 = dados_entre_200_e_400_(df_periodo)

    df_acima_de_400 = dados_acima_de_400_(df_periodo)

    return {
        "dados_abaixo_de_200": df_abaixo_de_200.to_dict("records"),
        "dados_entre_200_e_400": df_entre_200_e_400.to_dict("records"),
        "dados_acima_de_400": df_acima_de_400.to_dict("records"),
    }
