"""Queries usadas na página Top 10 Marcas Período."""


def query_top_10_marcas_periodo() -> str:
    """Query para calcular os dados de um determinado período.

    Returns:
        str: Query com os dados de um determinado período.
    """
    return """
    SELECT
        t.marca AS Marca
        , t.porcentagem AS Porcentagem
    FROM
        top_10_marcas_periodo('', $data_inicio, $data_fim) AS t
    ORDER BY
        t.porcentagem DESC
    LIMIT
        10;
    """
