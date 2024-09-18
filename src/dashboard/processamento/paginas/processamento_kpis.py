from duckdb import DuckDBPyConnection

from dashboard.processamento.queries import queries_kpis


def numero_produtos_e_media_precos_hoje(
    conexao: DuckDBPyConnection,
) -> list[str]:
    query = queries_kpis.query_numero_produtos_e_media_precos_hoje()

    return conexao.sql(query).fetchall()[0]


def media_produtos_e_media_precos_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> list[str]:
    query = queries_kpis.query_media_produtos_e_media_precos_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return conexao.execute(query, parametros).fetchall()[0]


def numero_marcas_hoje(conexao: DuckDBPyConnection) -> str:
    query = queries_kpis.query_numero_marcas_hoje()

    return str(conexao.sql(query).fetchall()[0][0])


def media_marcas_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> str:
    query = queries_kpis.query_media_marcas_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return str(conexao.execute(query, parametros).fetchall()[0][0])


def numero_produtos_em_promocao_e_percentual_medio_desconto_hoje(
    conexao: DuckDBPyConnection,
) -> list[str]:
    query = queries_kpis.query_numero_produtos_em_promocao_e_percentual_medio_desconto_hoje()

    return conexao.sql(query).fetchall()[0]


def media_produtos_em_promocao_e_percentual_medio_desconto_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> list[str]:
    query = queries_kpis.query_media_produtos_em_promocao_e_media_percentual_desconto_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return conexao.execute(query, parametros).fetchall()[0]


def numero_marcas_em_promocao_hoje(conexao: DuckDBPyConnection) -> str:
    query = queries_kpis.query_numero_marcas_em_promocao_hoje()

    return str(conexao.sql(query).fetchall()[0][0])


def media_marcas_em_promocao_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> str:
    query = queries_kpis.query_media_marcas_em_promocao_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return str(conexao.execute(query, parametros).fetchall()[0][0])


def numero_produtos_abaixo_de_200_reais_hoje(
    conexao: DuckDBPyConnection,
) -> str:
    query = queries_kpis.query_numero_produtos_abaixo_de_200_reais_hoje()

    return str(conexao.sql(query).fetchall()[0][0])


def media_produtos_abaixo_de_200_reais_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> str:
    query = queries_kpis.query_media_produtos_abaixo_de_200_reais_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return str(conexao.execute(query, parametros).fetchall()[0][0])


def numero_produtos_com_20_ou_mais_avaliacoes_hoje(
    conexao: DuckDBPyConnection,
) -> str:
    query = queries_kpis.query_numero_produtos_com_20_ou_mais_avaliacoes_hoje()

    return str(conexao.sql(query).fetchall()[0][0])


def media_produtos_com_20_ou_mais_avaliacoes_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> str:
    query = (
        queries_kpis.query_media_produtos_com_20_ou_mais_avaliacoes_periodo()
    )

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return str(conexao.execute(query, parametros).fetchall()[0][0])


def numero_produtos_sem_avaliacoes_hoje(conexao: DuckDBPyConnection) -> str:
    query = queries_kpis.query_numero_produtos_sem_avaliacoes_hoje()

    return str(conexao.sql(query).fetchall()[0][0])


def media_produtos_sem_avaliacoes_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> str:
    query = queries_kpis.query_media_produtos_sem_avaliacoes_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return str(conexao.execute(query, parametros).fetchall()[0][0])


def numero_produtos_com_nota_superior_4_hoje(
    conexao: DuckDBPyConnection,
) -> str:
    query = queries_kpis.query_numero_produtos_com_nota_superior_4_hoje()

    return str(conexao.sql(query).fetchall()[0][0])


def media_produtos_com_nota_superior_4_periodo(
    conexao: DuckDBPyConnection, data_inicio: str, data_fim: str
) -> str:
    query = queries_kpis.query_media_produtos_com_nota_superior_4_periodo()

    parametros = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return str(conexao.execute(query, parametros).fetchall()[0][0])


def dados_hoje(conexao: DuckDBPyConnection) -> dict[str, str]:
    lista_um = numero_produtos_e_media_precos_hoje(conexao)

    num_produtos = lista_um[0]

    media_precos = lista_um[1]

    lista_dois = numero_produtos_em_promocao_e_percentual_medio_desconto_hoje(
        conexao
    )

    num_produtos_promocoes = lista_dois[0]

    percentual_medio_desconto = lista_dois[1]

    num_marcas = numero_marcas_hoje(conexao)

    num_marcas_promocoes = numero_marcas_em_promocao_hoje(conexao)

    produtos_abaixo_de_200_reais = numero_produtos_abaixo_de_200_reais_hoje(
        conexao
    )

    produtos_20_ou_mais_avaliacoes = (
        numero_produtos_com_20_ou_mais_avaliacoes_hoje(conexao)
    )

    produtos_sem_avaliacao = numero_produtos_sem_avaliacoes_hoje(conexao)

    produtos_com_nota_maior_que_4 = numero_produtos_com_nota_superior_4_hoje(
        conexao
    )

    return {
        "num_produtos": num_produtos,
        "media_precos": media_precos,
        "produtos_promocoes": num_produtos_promocoes,
        "percentual_medio_desconto": percentual_medio_desconto,
        "num_marcas": num_marcas,
        "marcas_promocoes": num_marcas_promocoes,
        "produtos_abaixo_200": produtos_abaixo_de_200_reais,
        "produtos_20_avaliacoes": produtos_20_ou_mais_avaliacoes,
        "produtos_sem_avaliacoes": produtos_sem_avaliacao,
        "produtos_nota_maior_4": produtos_com_nota_maior_que_4,
    }


def dados_periodo(
    conexao: DuckDBPyConnection,
    data_inicio: str,
    data_fim: str,
) -> dict[str, str]:
    lista_um = media_produtos_e_media_precos_periodo(
        conexao, data_inicio, data_fim
    )

    num_produtos = lista_um[0]
    media_precos = lista_um[1]

    lista_dois = media_produtos_em_promocao_e_percentual_medio_desconto_periodo(
        conexao, data_inicio, data_fim
    )

    num_produtos_promocoes = lista_dois[0]
    percentual_medio_desconto = lista_dois[1]

    num_marcas = media_marcas_periodo(conexao, data_inicio, data_fim)

    num_marcas_promocoes = media_marcas_em_promocao_periodo(
        conexao, data_inicio, data_fim
    )

    produtos_abaixo_de_200_reais = media_produtos_abaixo_de_200_reais_periodo(
        conexao, data_inicio, data_fim
    )

    produtos_20_ou_mais_avaliacoes = (
        media_produtos_com_20_ou_mais_avaliacoes_periodo(
            conexao, data_inicio, data_fim
        )
    )

    produtos_sem_avaliacao = media_produtos_sem_avaliacoes_periodo(
        conexao, data_inicio, data_fim
    )

    produtos_com_nota_maior_que_4 = media_produtos_com_nota_superior_4_periodo(
        conexao, data_inicio, data_fim
    )

    return {
        "num_produtos": num_produtos,
        "media_precos": media_precos,
        "produtos_promocoes": num_produtos_promocoes,
        "percentual_medio_desconto": percentual_medio_desconto,
        "num_marcas": num_marcas,
        "marcas_promocoes": num_marcas_promocoes,
        "produtos_abaixo_200": produtos_abaixo_de_200_reais,
        "produtos_20_avaliacoes": produtos_20_ou_mais_avaliacoes,
        "produtos_sem_avaliacoes": produtos_sem_avaliacao,
        "produtos_nota_maior_4": produtos_com_nota_maior_que_4,
    }
