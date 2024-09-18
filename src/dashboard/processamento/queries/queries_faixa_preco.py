def query_faixas_preco_hoje() -> str:
    query = """
    SELECT
        dmr.marca
        , CASE
            WHEN dmr.preco_atual < 200 THEN '200'
            WHEN dmr.preco_atual BETWEEN 200 AND 400 THEN '200_400'
            ELSE '400'
          END AS faixa_preco
        , COUNT(*) AS num_produtos
    FROM
        dados_mais_recentes AS dmr
    GROUP BY
        dmr.marca
        , faixa_preco;
    """

    return query


def query_faixas_preco_periodo() -> str:
    query = """
    SELECT
        fpp.marca
        , fpp.faixa_preco
        , fpp.num_produtos
    FROM
        faixa_preco_periodo($data_inicio, $data_fim) AS fpp;
    """

    return query
