"""Queries usadas na página Preço Médio."""


def query_preco_medio_hoje() -> str:
    """Query para calcular os dados da coluna 'hoje'.

    Returns:
        str: Query com os dados de 'hoje'.
    """
    return """
    SELECT
        dmr.marca
        , AVG(dmr.preco_atual) AS preco_medio
        , COUNT(*) AS num_produtos
    FROM
        dados_mais_recentes AS dmr
    GROUP BY
        dmr.marca;
    """


def query_preco_medio_periodo() -> str:
    """Query para calcular os dados de um determinado período.

    Returns:
        str: Query com os dados de um determinado período.
    """
    return """
    SELECT
        pm.marca
        , pm.preco_medio
        , pm.num_produtos
    FROM
        preco_medio_periodo($data_inicio, $data_fim) AS pm;
    """
