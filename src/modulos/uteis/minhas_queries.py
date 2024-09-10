def kpi_num_total_itens() -> str:
    query = """
    SELECT
        count(*) AS "Número Total de Produtos"
    FROM
        dados_mais_recentes;
    """

    return query


def kpi_num_marcas_unicas() -> str:
    query = """
    SELECT
        COUNT(DISTINCT marca) AS "Número de Marcas"
    FROM
        dados_mais_recentes
    WHERE
        marca <> 'GENERICA';
    """

    return query


def kpi_preco_atual_medio() -> str:
    query = """
    SELECT
        AVG(preco_atual) AS "Média Preço"
    FROM
        dados_mais_recentes;
    """

    return query


def marcas_mais_encontradas() -> str:
    query = """
    SELECT
        marca AS "Marca"
        , COUNT(marca) AS "Qtd Produtos"
    FROM
        dados_mais_recentes
    GROUP BY
        marca
    ORDER BY
        "Qtd Produtos" DESC
        , marca ASC
    LIMIT
        10;
    """

    return query


def preco_medio_por_marca() -> str:
    query = """
    SELECT
        marcas as "Marca"
        , AVG(preco_atual) AS "Preço Médio"
    FROM
        dados_mais_recentes
    GROUP BY
        marca
    ORDER BY
        "Preço Médio" DESC
        , marca ASC;
    """

    return query


def satisfacao_media_por_marca() -> str:
    query = """
    SELECT
        marca as "Marca"
        , AVG(nota_avalicao) as "Satisfação Média"
    FROM
        dados_mais_recentes
    WHERE
        num_avaliacoes >= 20
    GROUP BY
        marca
    ORDER BY
        "Satisfação Média" DESC
        , marca ASC;
    """

    return query


def cast_polars_entrada() -> str:
    query = """
    SELECT
        marca
        , produto
        , preco_velho_reais
        , preco_velho_centavos
        , preco_atual_reais
        , preco_atual_centavos
        , nota_avaliacao
        , num_avaliacoes
        , _fonte
        , _site
        , STRFTIME(_data_coleta, '%Y-%m-%d %H:%M:%S') as _data_coleta
        , _pagina
        , _ordem
    FROM
        df;
    """

    return query


def cast_polars_saida() -> str:
    query = """
    SELECT
        marca
        , produto
        , preco_velho::FLOAT4 AS preco_velho
        , preco_atual::FLOAT4 AS preco_atual
        , promocao
        , percentual_promocao::FLOAT4 AS percentual_promocao
        , nota_avaliacao::FLOAT4 AS nota_avaliacao
        , num_avaliacoes::INT4 AS num_avaliacoes
        , _fonte
        , _site
        , _data_coleta
        , _horario_coleta
        , _pagina::INT1 AS _pagina
        , _ordem::INT1 AS _ordem
    FROM
        df;
    """

    return query
