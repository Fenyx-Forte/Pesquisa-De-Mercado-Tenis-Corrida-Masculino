"""Queries usadas na página Promoções."""


def query_promocao_hoje() -> str:
    """Query para calcular os dados da coluna 'hoje'.

    Returns:
        str: Query com os dados de 'hoje'.
    """
    return """
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


def query_promocao_periodo() -> str:
    """Query para calcular os dados de um determinado período.

    Returns:
        str: Query com os dados de um determinado período.
    """
    return """
    SELECT
        m.marca
        , m.produtos
        , m.desconto
    FROM
        media_promocoes_periodo($data_inicio, $data_fim) AS m;
    """
