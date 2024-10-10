from duckdb import DuckDBPyConnection
from pandas import DataFrame as pd_DataFrame

from dashboard.processamento.queries import queries_preco_medio


def calcular_df_hoje(conexao: DuckDBPyConnection) -> pd_DataFrame:
    query = queries_preco_medio.query_preco_medio_hoje()

    return conexao.sql(query).df()


def calcular_df_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> pd_DataFrame:
    query = queries_preco_medio.query_preco_medio_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return conexao.execute(query, parametros).df()


def dados_abaixo_de_200(df: pd_DataFrame) -> pd_DataFrame:
    return df.loc[df["preco_medio"] < 200].sort_values(
        by=["num_produtos", "preco_medio", "marca"],
        ascending=[False, True, True],
    )


def dados_entre_200_e_400_(df: pd_DataFrame) -> pd_DataFrame:
    return df.loc[df["preco_medio"].between(200, 400)].sort_values(
        by=["num_produtos", "preco_medio", "marca"],
        ascending=[False, True, True],
    )


def dados_acima_de_400_(df: pd_DataFrame) -> pd_DataFrame:
    return df.loc[df["preco_medio"] > 400].sort_values(
        by=["num_produtos", "preco_medio", "marca"],
        ascending=[False, True, True],
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


def calcula_linha_totais(dados: list[dict]) -> dict:
    soma_num_produtos = 0
    media_preco_medio = 0

    if len(dados) == 0:
        return {
            "marca": "TOTAL",
            "num_produtos": soma_num_produtos,
            "preco_medio": media_preco_medio,
        }

    df = pd_DataFrame(dados)

    soma_num_produtos = df["num_produtos"].sum()
    media_preco_medio = (
        df["preco_medio"] * df["num_produtos"]
    ).sum() / soma_num_produtos

    return {
        "marca": "TOTAL",
        "num_produtos": soma_num_produtos,
        "preco_medio": media_preco_medio,
    }
