def query_promocao_hoje() -> str:
    query = """
    SELECT
        dmr.marca
        , COUNT(*) AS produtos
        , AVG(dmr.percentual_promocao * 100) AS desconto
    FROM
        dados_mais_recentes AS dmr
    WHERE
        dmr.promocao = true
    GROUP BY
        dmr.marca
    ORDER BY
        produtos DESC
        , desconto DESC
        , dmr.marca ASC;
    """

    return query


def query_promocao_periodo() -> str:
    query = """
    SELECT
        m.marca
        , m.produtos
        , m.desconto
    FROM
        media_promocoes_periodo($data_inicio, $data_fim) AS M
    ORDER BY
        m.produtos DESC
        , m.desconto DESC
        , m.marca ASC;
    """

    return query
