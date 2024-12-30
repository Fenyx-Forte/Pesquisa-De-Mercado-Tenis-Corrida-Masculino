"""Módulo de queries para dataframes do Polars na entrada e saída do ETL do webscraping utilizando o Polars.

Essas queries são utilizadas para transformar os dataframes do DuckDB em dataframes do Polars, para que o contrato de dados
possa ser aplicado a fim de verificar se o ETL foi bem sucedido.
"""


def cast_polars_entrada() -> str:
    """Transforma o dataframe do DuckDB para Polars no início do ETL."""
    return """
    SELECT
        marca
        , produto
        , preco_velho_reais
        , preco_velho_centavos
        , preco_atual_reais
        , preco_atual_centavos
        , nota_avaliacao
        , num_avaliacoes
        , STRFTIME(_data_coleta, '%Y-%m-%d %H:%M:%S') as _data_coleta
        , _pagina
        , _ordem
    FROM
        df;
    """


def cast_polars_saida() -> str:
    """Transforma o dataframe do DuckDB para Polars no fim do ETL."""
    return """
    SELECT
        marca
        , produto
        , preco_velho::FLOAT4 AS preco_velho
        , preco_atual::FLOAT4 AS preco_atual
        , promocao
        , percentual_promocao::FLOAT4 AS percentual_promocao
        , nota_avaliacao::FLOAT4 AS nota_avaliacao
        , num_avaliacoes::INT4 AS num_avaliacoes
        , _data_coleta
        , _horario_coleta
        , _pagina::INT1 AS _pagina
        , _ordem::INT1 AS _ordem
    FROM
        df;
    """
