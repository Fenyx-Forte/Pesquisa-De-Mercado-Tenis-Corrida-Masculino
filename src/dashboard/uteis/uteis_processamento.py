from datetime import datetime

from dash import ClientsideFunction


def callback_atualizar_titulo_pagina() -> ClientsideFunction:
    return ClientsideFunction(
        namespace="clientside",
        function_name="atualizar_titulo_pagina",
    )


def callback_abrir_e_fechar_sidebar() -> ClientsideFunction:
    return ClientsideFunction(
        namespace="clientside",
        function_name="abrir_e_fechar_sidebar",
    )


def callback_fechar_sidebar() -> ClientsideFunction:
    return ClientsideFunction(
        namespace="clientside",
        function_name="fechar_sidebar",
    )


def callback_verificar_datas() -> ClientsideFunction:
    return ClientsideFunction(
        namespace="clientside",
        function_name="verificar_datas",
    )


def callback_abrir_modal() -> ClientsideFunction:
    return ClientsideFunction(
        namespace="clientside",
        function_name="abrir_modal",
    )


def callback_ranking_direto_valores() -> ClientsideFunction:
    return ClientsideFunction(
        namespace="clientside",
        function_name="ranking_direto",
    )


def callback_ranking_inverso_valores() -> ClientsideFunction:
    return ClientsideFunction(
        namespace="clientside",
        function_name="ranking_inverso",
    )


def callback_linha_totais_preco_medio() -> ClientsideFunction:
    return ClientsideFunction(
        namespace="clientside",
        function_name="linha_totais_preco_medio",
    )


def callback_linha_totais_faixa_preco() -> ClientsideFunction:
    return ClientsideFunction(
        namespace="clientside",
        function_name="linha_totais_faixa_preco",
    )


def callback_linha_totais_satisfacao() -> ClientsideFunction:
    return ClientsideFunction(
        namespace="clientside",
        function_name="linha_totais_satisfacao",
    )


def callback_linha_totais_promocoes() -> ClientsideFunction:
    return ClientsideFunction(
        namespace="clientside",
        function_name="linha_totais_promocoes",
    )


def valida_data(data_str: str) -> bool:
    # Valida se a string representa uma data válida no formato YYYY-MM-DD.
    formato = "%Y-%m-%d"

    try:
        # Tenta converter a string para uma data.
        datetime.strptime(data_str, formato)

        return True  # Data válida.

    except:
        return False  # Data inválida.


def valida_periodo(
    data_inicio: str,
    data_fim: str,
    data_coleta_mais_antiga: str,
    data_coleta_mais_recente: str,
) -> bool:
    formato = "%Y-%m-%d"

    data_inicio_time = datetime.strptime(data_inicio, formato)

    data_fim_time = datetime.strptime(data_fim, formato)

    data_coleta_mais_antiga_time = datetime.strptime(
        data_coleta_mais_antiga, formato
    )

    data_coleta_mais_recente_time = datetime.strptime(
        data_coleta_mais_recente, formato
    )

    return (
        (data_inicio_time <= data_fim_time)
        and (data_inicio_time >= data_coleta_mais_antiga_time)
        and (data_fim_time <= data_coleta_mais_recente_time)
    )


def valida_entrada_datas(
    data_inicio: str,
    data_fim: str,
    data_coleta_mais_antiga: str,
    data_coleta_mais_recente: str,
) -> bool:
    if not (valida_data(data_inicio) and valida_data(data_fim)):
        return False

    return valida_periodo(
        data_inicio=data_inicio,
        data_fim=data_fim,
        data_coleta_mais_antiga=data_coleta_mais_antiga,
        data_coleta_mais_recente=data_coleta_mais_recente,
    )


def formatar_data_pt_br(data: str) -> str:
    # "data" esta no formato YYYY-MM-DD
    componentes = data.split("-")
    dia = componentes[2]
    mes = componentes[1]
    ano = componentes[0]

    return f"{dia}/{mes}/{ano}"


def retorna_periodo(data_inicio: str, data_fim: str) -> str:
    data_inicio_formatada = formatar_data_pt_br(data_inicio)
    data_fim_formatada = formatar_data_pt_br(data_fim)

    return f"{data_inicio_formatada} - {data_fim_formatada}"
