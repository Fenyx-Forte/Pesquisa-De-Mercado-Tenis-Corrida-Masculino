"""Queries usadas na página KPI's."""


def query_kpis_hoje() -> str:
    """Query para calcular os dados da coluna 'hoje'.

    Returns:
        str: Query com os dados de 'hoje'.
    """
    return """
    SELECT
        COUNT(*) AS numero_produtos
        , FORMAT(
            '{:.2f}'
            , AVG(dmr.preco_atual)
        ) AS media_precos
        , COUNT(
            DISTINCT
                CASE
                    WHEN dmr.marca <> 'GENERICA'
                        THEN dmr.marca
                END
        ) AS numero_marcas
        , COUNT(
            CASE
                WHEN dmr.promocao = true
                    THEN 1
            END
        ) AS numero_produtos_em_promocao
        , FORMAT(
            '{:.2f}'
            , AVG(
                CASE
                    WHEN dmr.promocao = true
                        THEN dmr.percentual_promocao
                END
            ) * 100
        ) AS percentual_medio_desconto
        , COUNT(
            DISTINCT
                CASE
                    WHEN dmr.promocao = true AND dmr.marca <> 'GENERICA'
                        THEN dmr.marca
                END
        ) AS numero_marcas_em_promocao
        , COUNT(
            CASE
                WHEN dmr.preco_atual < 200
                    THEN 1
            END
        ) AS numero_produtos_abaixo_de_200_reais
        , COUNT(
            CASE
                WHEN dmr.num_avaliacoes >= 20
                    THEN 1
            END
        ) AS numero_produtos_com_20_ou_mais_avaliacoes
        , COUNT(
            CASE
                WHEN dmr.num_avaliacoes = 0
                    THEN 1
            END
        ) AS numero_produtos_sem_avaliacoes
        , COUNT(
            CASE
                WHEN dmr.num_avaliacoes > 0 AND dmr.nota_avaliacao > 4
                    THEN 1
            END
        ) AS numero_produtos_com_nota_superior_4
    FROM
        dados_mais_recentes AS dmr;
    """


def query_kpis_periodo() -> str:
    """Query para calcular os dados de um determinado período.

    Returns:
        str: Query com os dados de um determinado período.
    """
    return """
    SELECT
        kp.numero_produtos
        , kp.media_precos
        , kp.numero_marcas
        , kp.numero_produtos_em_promocao
        , kp.percentual_medio_desconto
        , kp.numero_marcas_em_promocao
        , kp.numero_produtos_abaixo_de_200_reais
        , kp.numero_produtos_com_20_ou_mais_avaliacoes
        , kp.numero_produtos_sem_avaliacoes
        , kp.numero_produtos_com_nota_superior_4
    FROM
        kpis_periodo($data_inicio, $data_fim) AS kp;
    """
