def query_preco_medio_hoje() -> str:
    query = """
    SELECT
        marca
        , AVG(preco_atual) AS preco_medio
        , COUNT(*) AS num_produtos
    FROM
        dados_mais_recentes
    GROUP BY
        marca;
    """

    return query


def query_preco_medio_periodo() -> str:
    query = """
    SELECT
        marca
        , preco_medio
        , num_produtos
    FROM
        preco_medio_e_num_produtos_periodo($data_inicio, $data_fim);
    """

    return query
