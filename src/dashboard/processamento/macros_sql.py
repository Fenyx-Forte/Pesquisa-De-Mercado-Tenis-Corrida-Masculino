def macro_dados_completos_por_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO dados_completos_por_periodo(data_inicio, data_fim) AS TABLE
        SELECT
            dc.marca
            , dc.preco_atual
            , dc.promocao
            , dc.percentual_promocao
            , dc.nota_avaliacao
            , dc.num_avaliacoes
            , dc.data_coleta
        FROM
            dados_completos AS dc
        WHERE
            dc.data_coleta BETWEEN data_inicio AND data_fim;
    """

    return query


def macro_top_10_marcas_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO top_10_marcas_periodo(periodo, data_inicio, data_fim) AS TABLE
        WITH porcentagem_por_dia AS (
            SELECT
                dcp.marca AS marca
                , (
                    COUNT(*) * 100.0 / (SUM(COUNT(*)) OVER(PARTITION BY dcp.data_coleta))
                ) AS porcentagem
            FROM
                dados_completos_por_periodo(data_inicio, data_fim) AS dcp
            GROUP BY
                dcp.data_coleta
                , dcp.marca
        )
        SELECT
            ppd.marca AS marca
            , AVG(ppd.porcentagem) AS porcentagem
            , periodo AS periodo
        FROM
            porcentagem_por_dia AS ppd
        GROUP BY
            ppd.marca;
    """

    return query


def macro_preco_medio_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO preco_medio_periodo(data_inicio, data_fim) AS TABLE
        SELECT
            dcp.marca AS marca
            , AVG(dcp.preco_atual) AS preco_medio
            , COUNT(*) / COUNT(DISTINCT dcp.data_coleta) AS num_produtos
        FROM
            dados_completos_por_periodo(data_inicio, data_fim) AS dcp
        GROUP BY
            dcp.marca;
    """

    return query


def macro_faixa_preco_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO faixa_preco_periodo(data_inicio, data_fim) AS TABLE
        SELECT
            dcp.marca AS marca
            , CASE
                WHEN dcp.preco_atual < 200 THEN '200'
                WHEN dcp.preco_atual BETWEEN 200 AND 400 THEN '200_400'
                ELSE '400'
              END AS faixa_preco
            , COUNT(*) / COUNT(DISTINCT dcp.data_coleta) AS num_produtos
        FROM
            dados_completos_por_periodo(data_inicio, data_fim) AS dcp
        GROUP BY
            dcp.marca
            , faixa_preco;
    """

    return query


def macro_media_avaliacoes_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO media_avaliacoes_periodo(data_inicio, data_fim) AS TABLE
        WITH media_avaliacoes_por_dia AS (
            SELECT
                dcp.marca AS marca
                , AVG(dcp.nota_avaliacao) AS media_avaliacao
                , AVG(dcp.num_avaliacoes) AS media_num_avaliacoes
            FROM
                dados_completos_por_periodo(data_inicio, data_fim) AS dcp
            WHERE
                dcp.num_avaliacoes > 0
            GROUP BY
                dcp.data_coleta
                , dcp.marca
        )
        SELECT
            mad.marca
            , AVG(mad.media_avaliacao) AS nota_avaliacao
            , AVG(mad.media_num_avaliacoes) AS num_avaliacoes
        FROM
            media_avaliacoes_por_dia AS mad
        GROUP BY
            mad.marca;
    """

    return query


def macro_media_promocoes_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO media_promocoes_periodo(data_inicio, data_fim) AS TABLE
        SELECT
            dcp.marca AS marca
            , COUNT(*) / COUNT(DISTINCT dcp.data_coleta) AS produtos
            , AVG(dcp.percentual_promocao * 100) AS desconto
        FROM
            dados_completos_por_periodo(data_inicio, data_fim) AS dcp
        WHERE
            dcp.promocao = true
        GROUP BY
            dcp.marca
        ORDER BY
            produtos DESC
            , desconto DESC
            , dcp.marca ASC;
    """

    return query
