from duckdb import DuckDBPyConnection

from dashboard.processamento.queries import queries_kpis


def dados_hoje(conexao: DuckDBPyConnection) -> dict[str, str]:
    query = queries_kpis.query_kpis_hoje()

    dados = conexao.sql(query).fetchall()[0]

    return {
        "num_produtos": str(dados[0]),
        "media_precos": str(dados[1]),
        "num_marcas": str(dados[2]),
        "produtos_promocoes": str(dados[3]),
        "percentual_medio_desconto": str(dados[4]),
        "marcas_promocoes": str(dados[5]),
        "produtos_abaixo_200": str(dados[6]),
        "produtos_20_avaliacoes": str(dados[7]),
        "produtos_sem_avaliacoes": str(dados[8]),
        "produtos_nota_maior_4": str(dados[9]),
    }


def dados_periodo(
    conexao: DuckDBPyConnection,
    data_inicio: str,
    data_fim: str,
) -> dict[str, str]:
    query = queries_kpis.query_kpis_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    dados = conexao.execute(query, parametros).fetchall()[0]

    return {
        "num_produtos": str(dados[0]),
        "media_precos": str(dados[1]),
        "num_marcas": str(dados[2]),
        "produtos_promocoes": str(dados[3]),
        "percentual_medio_desconto": str(dados[4]),
        "marcas_promocoes": str(dados[5]),
        "produtos_abaixo_200": str(dados[6]),
        "produtos_20_avaliacoes": str(dados[7]),
        "produtos_sem_avaliacoes": str(dados[8]),
        "produtos_nota_maior_4": str(dados[9]),
    }
