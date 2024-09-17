def query_preco_medio_hoje() -> str:
    query = """
    SELECT
        dmr.marca
        , AVG(dmr.preco_atual) AS preco_medio
        , COUNT(*) AS num_produtos
    FROM
        dados_mais_recentes AS dmr
    GROUP BY
        dmr.marca;
    """

    return query


def query_preco_medio_periodo() -> str:
    query = """
    SELECT
        pm.marca
        , pm.preco_medio
        , pm.num_produtos
    FROM
        preco_medio_e_num_produtos_periodo($data_inicio, $data_fim) AS pm;
    """

    return query
