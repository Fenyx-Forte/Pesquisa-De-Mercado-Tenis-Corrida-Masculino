def regexp_replace(coluna: str, padrao: str, substituicao: str):
    return f"regexp_replace({coluna}, '{padrao}', '{substituicao}', 'g')"


def tratar_coluna_string(nome_coluna: str) -> str:
    maiusculo = f"upper({nome_coluna})"
    tratar_a = regexp_replace(maiusculo, "[ÁÀÂÃÄÅ]", "A")
    tratar_e = regexp_replace(tratar_a, "[ÉÈÊË]", "E")
    tratar_i = regexp_replace(tratar_e, "[ÍÌÎÏ]", "I")
    tratar_o = regexp_replace(tratar_i, "[ÓÒÔÕÖ]", "O")
    tratar_u = regexp_replace(tratar_o, "[ÚÙÛÜ]", "U")
    tratar_c = f"replace({tratar_u}, 'Ç', 'C')"
    remover_caracteres_especiais = regexp_replace(tratar_c, "[^A-Z0-9 ]", " ")
    remover_espacos_em_branco = regexp_replace(
        remover_caracteres_especiais, "\\s+", " "
    )

    coluna_tratada = f"""
        trim({remover_espacos_em_branco})
    """

    return coluna_tratada


def tratar_marca() -> str:
    coluna_tratada = f"""
    ifnull(
        {tratar_coluna_string("marca")},
        'GENERICA'
    ) as marca
    """

    return coluna_tratada


def tratar_produto() -> str:
    coluna_tratada = f"""
    ifnull(
        {tratar_coluna_string("produto")},
        'PRODUTO SEM NOME'
    ) as produto
    """

    return coluna_tratada


def adicionar_preco_completo(
    col_preco_reais: str,
    col_preco_centavos: str,
    nome_coluna_nova: str,
) -> str:
    coluna_nova = f"""
    cast(
        (case
            when {col_preco_reais} is not null and {col_preco_centavos} is not null
                then concat(replace({col_preco_reais}, '.', ''), '.', {col_preco_centavos})
            else
                {col_preco_reais}
        end) as DECIMAL(9, 2)
    ) as {nome_coluna_nova}
    """

    return coluna_nova


def adicionar_preco_velho() -> str:
    coluna_nova = adicionar_preco_completo(
        "preco_velho_reais", "preco_velho_centavos", "preco_velho"
    )

    return coluna_nova


def tratar_preco_velho() -> str:
    coluna_tratada = """
    case
        when preco_velho is null then preco_atual
        else preco_velho
    end as preco_velho
    """

    return coluna_tratada


def adicionar_preco_atual() -> str:
    coluna_nova = adicionar_preco_completo(
        "preco_atual_reais", "preco_atual_centavos", "preco_atual"
    )

    return coluna_nova


def adicionar_promocao() -> str:
    coluna_nova = """
    (preco_velho_reais is not null) as promocao
    """

    return coluna_nova


def adicionar_percentual_promocao() -> str:
    coluna_nova = """
    cast(
        (case
            when promocao = true then ( (preco_velho - preco_atual) / preco_velho) * 100
            else 0
        end) as DECIMAL(4, 2)
    ) as percentual_promocao
    """

    return coluna_nova


def tratar_nota_avaliacao() -> str:
    coluna_tratada = """
    cast(
        ifnull(nota_avaliacao, '0')
        as DECIMAL(4, 2)
    ) as nota_avaliacao
    """

    return coluna_tratada


def tratar_num_avaliacoes() -> str:
    coluna_tratada = """
    cast(
        ifnull(trim(BOTH '()' from num_avaliacoes), '0')
        as UINTEGER
    ) as num_avaliacoes
    """

    return coluna_tratada


def tratar_fonte() -> str:
    coluna_tratada = """
        _fonte
    """

    return coluna_tratada


def tratar_site() -> str:
    coluna_tratada = """
        _site
    """

    return coluna_tratada


def tratar_data_coleta() -> str:
    coluna_tratada = """
        _data_coleta
    """

    return coluna_tratada


def tratar_pagina() -> str:
    coluna_tratada = """
        cast(_pagina as UTINYINT) as _pagina
    """

    return coluna_tratada


def tratar_ordem() -> str:
    coluna_tratada = """
        cast(_ordem as UTINYINT) as _ordem
    """

    return coluna_tratada
