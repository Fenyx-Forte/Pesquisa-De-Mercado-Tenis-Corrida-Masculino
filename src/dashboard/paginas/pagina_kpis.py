"""Página KPI's."""

from dash import (
    Input,
    Output,
    State,
    callback,
    clientside_callback,
    html,
    register_page,
)
from dash.exceptions import PreventUpdate
from dash_bootstrap_components import (
    Col,
    Row,
)

from dashboard.processamento import gerenciador
from dashboard.uteis import componentes_pagina, uteis_processamento

register_page(
    __name__,
    path="/kpis",
    name="KPI's",
    title="KPI's",
    description="Página KPI's",
    image_url="https://analise-de-dados-tenis-corrida.onrender.com/assets/images/imagem_link.jpg",
)


def id_pagina() -> str:
    """Id da página.

    Returns:
        str: id da página.
    """
    return "kpis"


def titulo_pagina() -> str:
    """Título da página.

    Returns:
        str: Título da página.
    """
    return "KPI's Principais"


def informacao(
    valor: str,
    id_informacao: str,
    sufixo_coluna: str,
) -> html.Div:
    """Div que representa 1 KPI.

    Args:
        valor (str): Valor a ser exibido na div.
        id_informacao (str): ID da div para identificar e manipular o conteúdo.
        sufixo_coluna (str): Sufixo que será adicionado ao id de cada Div.

    Returns:
        html.Div: Div representando 1 KPI.
    """
    return html.Div(
        [
            html.Div(
                valor,
                className="valor_cartao",
                id=f"{id_pagina()}_valor_{id_informacao}_{sufixo_coluna}",
            ),
            html.Div(
                html.I(className="fa-solid fa-trophy"),
                className="ranking_cartao",
                id=f"{id_pagina()}_ranking_{id_informacao}_{sufixo_coluna}",
            ),
        ],
        className="informacao",
    )


def coluna(
    sufixo_coluna: str,
    titulo_cabecalho: str,
    periodo: str,
    num_produtos: str,
    num_marcas: str,
    produtos_promocoes: str,
    marcas_promocoes: str,
    produtos_abaixo_200: str,
    percentual_medio_desconto: str,
    media_precos: str,
    produtos_20_avaliacoes: str,
    produtos_sem_avaliacoes: str,
    produtos_nota_maior_4: str,
) -> html.Div:
    """Retorna uma das 3 colunas usadas no corpo da página.

    Args:
        sufixo_coluna (str): Sufixo de cada coluna.
        titulo_cabecalho (str): Título do cabeçalho da coluna.
        periodo (str): Período utilizado para filtrar os dados.
        num_produtos (str): Número total de produtos.
        num_marcas (str): Número total de marcas.
        produtos_promocoes (str): Quantidade de produtos em promoção.
        marcas_promocoes (str): Quantidade de marcas com produtos em promoção.
        produtos_abaixo_200 (str): Número de produtos abaixo de 200 reais.
        percentual_medio_desconto (str): Percentual médio de desconto aplicado.
        media_precos (str): Média dos preços dos produtos.
        produtos_20_avaliacoes (str): Número de produtos com mais de 20 avaliações.
        produtos_sem_avaliacoes (str): Número de produtos sem avaliações.
        produtos_nota_maior_4 (str): Número de produtos com nota superior a 4.

    Returns:
        html.Div: Coluna.
    """
    return html.Div(
        [
            componentes_pagina.cabecalho_coluna(
                id_pagina=id_pagina(),
                sufixo_coluna=sufixo_coluna,
                titulo=titulo_cabecalho,
                periodo=periodo,
            ),
            componentes_pagina.conteiner_informacao(
                titulo_informacao="Número Produtos",
                informacao=informacao(
                    valor=num_produtos,
                    sufixo_coluna=sufixo_coluna,
                    id_informacao="num_produtos",
                ),
            ),
            componentes_pagina.conteiner_informacao(
                titulo_informacao="Número Marcas",
                informacao=informacao(
                    valor=num_marcas,
                    sufixo_coluna=sufixo_coluna,
                    id_informacao="num_marcas",
                ),
            ),
            componentes_pagina.conteiner_informacao(
                titulo_informacao="Produtos Abaixo De R$ 200,00",
                informacao=informacao(
                    valor=produtos_abaixo_200,
                    sufixo_coluna=sufixo_coluna,
                    id_informacao="produtos_abaixo_200",
                ),
            ),
            componentes_pagina.conteiner_informacao(
                titulo_informacao="Média Preços",
                informacao=informacao(
                    valor=media_precos,
                    sufixo_coluna=sufixo_coluna,
                    id_informacao="media_precos",
                ),
            ),
            componentes_pagina.conteiner_informacao(
                titulo_informacao="Produtos Com 20 Ou Mais Avaliações",
                informacao=informacao(
                    valor=produtos_20_avaliacoes,
                    sufixo_coluna=sufixo_coluna,
                    id_informacao="produtos_20_avaliacoes",
                ),
            ),
            componentes_pagina.conteiner_informacao(
                titulo_informacao="Produtos Com Nota Maior Que 4",
                informacao=informacao(
                    valor=produtos_nota_maior_4,
                    sufixo_coluna=sufixo_coluna,
                    id_informacao="produtos_nota_maior_4",
                ),
            ),
            componentes_pagina.conteiner_informacao(
                titulo_informacao="Produtos Sem Avaliações",
                informacao=informacao(
                    valor=produtos_sem_avaliacoes,
                    sufixo_coluna=sufixo_coluna,
                    id_informacao="produtos_sem_avaliacoes",
                ),
            ),
            componentes_pagina.conteiner_informacao(
                titulo_informacao="Produtos Em Promoção",
                informacao=informacao(
                    valor=produtos_promocoes,
                    sufixo_coluna=sufixo_coluna,
                    id_informacao="produtos_promocoes",
                ),
            ),
            componentes_pagina.conteiner_informacao(
                titulo_informacao="Marcas Em Promoção",
                informacao=informacao(
                    valor=marcas_promocoes,
                    sufixo_coluna=sufixo_coluna,
                    id_informacao="marcas_promocoes",
                ),
            ),
            componentes_pagina.conteiner_informacao(
                titulo_informacao="Média Desconto",
                informacao=informacao(
                    valor=percentual_medio_desconto,
                    sufixo_coluna=sufixo_coluna,
                    id_informacao="percentual_medio_desconto",
                ),
            ),
        ],
    )


def colunas() -> Row:
    """Retorna um conjunto de colunas.

    Returns:
        Row: Linha que contém todas as colunas do corpo da página.
    """
    periodo_hoje = gerenciador.retorna_periodo_hoje()

    periodo_escolhido = gerenciador.retorna_periodo_ultima_semana()

    periodo_historico = gerenciador.retorna_periodo_historico()

    dados_hoje = gerenciador.pagina_kpis_dados_hoje()

    dados_escolhido = gerenciador.pagina_kpis_dados_ultima_semana()

    dados_historico = gerenciador.pagina_kpis_dados_historico()

    return Row(
        [
            Col(
                coluna(
                    sufixo_coluna="hoje",
                    titulo_cabecalho="Hoje",
                    periodo=periodo_hoje,
                    **dados_hoje,
                ),
                xs=12,
                sm=6,
                md=4,
                class_name="coluna_hoje",
            ),
            Col(
                coluna(
                    sufixo_coluna="escolhido",
                    titulo_cabecalho="Período Escolhido",
                    periodo=periodo_escolhido,
                    **dados_escolhido,
                ),
                xs=12,
                sm=6,
                md=4,
                class_name="coluna_escolhido",
            ),
            Col(
                coluna(
                    sufixo_coluna="historico",
                    titulo_cabecalho="Histórico",
                    periodo=periodo_historico,
                    **dados_historico,
                ),
                xs=12,
                sm=6,
                md=4,
                class_name="coluna_historico",
            ),
        ],
        class_name="linha_colunas",
    )


layout = html.Div(
    [
        componentes_pagina.div_titulo(titulo_pagina()),
        componentes_pagina.div_seletor_datas_e_botao(
            id_pagina=id_pagina(),
            data_mais_antiga=gerenciador.retorna_data_coleta_mais_antiga(),
            data_mais_recente=gerenciador.retorna_data_coleta_mais_recente(),
        ),
        componentes_pagina.modal_erro(id_pagina()),
        colunas(),
    ],
    className="pagina",
    id=id_pagina(),
)

clientside_callback(
    uteis_processamento.callback_verificar_datas(),
    Output(f"{id_pagina()}_modal_erro_titulo", "children"),
    Output(f"{id_pagina()}_modal_erro_conteudo", "children"),
    Input(f"{id_pagina()}_botao", "n_clicks"),
    State(f"{id_pagina()}_seletor_datas", "start_date"),
    State(f"{id_pagina()}_seletor_datas", "end_date"),
    State(f"{id_pagina()}_periodo_hoje", "children"),
    State(f"{id_pagina()}_periodo_escolhido", "children"),
    State(f"{id_pagina()}_periodo_historico", "children"),
    prevent_initial_call=True,
)


@callback(
    Output(f"{id_pagina()}_valor_num_produtos_escolhido", "children"),
    Output(f"{id_pagina()}_valor_num_marcas_escolhido", "children"),
    Output(f"{id_pagina()}_valor_produtos_abaixo_200_escolhido", "children"),
    Output(f"{id_pagina()}_valor_media_precos_escolhido", "children"),
    Output(f"{id_pagina()}_valor_produtos_20_avaliacoes_escolhido", "children"),
    Output(f"{id_pagina()}_valor_produtos_nota_maior_4_escolhido", "children"),
    Output(
        f"{id_pagina()}_valor_produtos_sem_avaliacoes_escolhido",
        "children",
    ),
    Output(f"{id_pagina()}_valor_produtos_promocoes_escolhido", "children"),
    Output(
        f"{id_pagina()}_valor_marcas_promocoes_escolhido",
        "children",
    ),
    Output(
        f"{id_pagina()}_valor_percentual_medio_desconto_escolhido",
        "children",
    ),
    Output(f"{id_pagina()}_seletor_datas", "start_date"),
    Output(f"{id_pagina()}_seletor_datas", "end_date"),
    Output(f"{id_pagina()}_periodo_escolhido", "children"),
    Input(f"{id_pagina()}_modal_erro_titulo", "children"),
    State(f"{id_pagina()}_seletor_datas", "start_date"),
    State(f"{id_pagina()}_seletor_datas", "end_date"),
    prevent_initial_call=True,
    running=[(Output(f"{id_pagina()}_botao", "disabled"), True, False)],
)
def kpis_atualizar_dados_escolhido(
    titulo: str,
    data_inicio: str,
    data_fim: str,
) -> list[str | None]:
    """Retorna os dados atualizados da coluna "escolhido" para um período especificado.

    Args:
        titulo (str): Título atual do modal_erro. Se não for igual a "", então houve algum erro detectado pelo modal_erro.
        data_inicio (str): Data de início do período a ser considerado.
        data_fim (str): Data de fim do período a ser considerado.

    Returns:
        list[str | None]: Lista com os dados necessários para atualizar a coluna.
    """
    if titulo != "":
        raise PreventUpdate

    if not gerenciador.valida_entrada_datas(data_inicio, data_fim):
        raise PreventUpdate

    periodo_novo = uteis_processamento.retorna_periodo(data_inicio, data_fim)

    dados_escolhido = gerenciador.pagina_kpis_atualiza_dados_escolhido(
        data_inicio,
        data_fim,
    )

    return [
        dados_escolhido["num_produtos"],
        dados_escolhido["num_marcas"],
        dados_escolhido["produtos_abaixo_200"],
        dados_escolhido["media_precos"],
        dados_escolhido["produtos_20_avaliacoes"],
        dados_escolhido["produtos_nota_maior_4"],
        dados_escolhido["produtos_sem_avaliacoes"],
        dados_escolhido["produtos_promocoes"],
        dados_escolhido["marcas_promocoes"],
        dados_escolhido["percentual_medio_desconto"],
        None,
        None,
        periodo_novo,
    ]


clientside_callback(
    uteis_processamento.callback_abrir_modal(),
    Output(f"{id_pagina()}_modal_erro", "is_open"),
    Input(f"{id_pagina()}_modal_erro_titulo", "children"),
    prevent_initial_call=True,
)


id_num_produtos = "num_produtos"
clientside_callback(
    uteis_processamento.callback_ranking_direto_valores(),
    Output(f"{id_pagina()}_ranking_{id_num_produtos}_escolhido", "className"),
    Output(f"{id_pagina()}_ranking_{id_num_produtos}_hoje", "className"),
    Output(f"{id_pagina()}_ranking_{id_num_produtos}_historico", "className"),
    Input(f"{id_pagina()}_valor_{id_num_produtos}_escolhido", "children"),
    State(f"{id_pagina()}_valor_{id_num_produtos}_hoje", "children"),
    State(f"{id_pagina()}_valor_{id_num_produtos}_historico", "children"),
)

id_num_marcas = "num_marcas"
clientside_callback(
    uteis_processamento.callback_ranking_direto_valores(),
    Output(f"{id_pagina()}_ranking_{id_num_marcas}_escolhido", "className"),
    Output(f"{id_pagina()}_ranking_{id_num_marcas}_hoje", "className"),
    Output(f"{id_pagina()}_ranking_{id_num_marcas}_historico", "className"),
    Input(f"{id_pagina()}_valor_{id_num_marcas}_escolhido", "children"),
    State(f"{id_pagina()}_valor_{id_num_marcas}_hoje", "children"),
    State(f"{id_pagina()}_valor_{id_num_marcas}_historico", "children"),
)

id_produtos_promocoes = "produtos_promocoes"
clientside_callback(
    uteis_processamento.callback_ranking_direto_valores(),
    Output(
        f"{id_pagina()}_ranking_{id_produtos_promocoes}_escolhido",
        "className",
    ),
    Output(f"{id_pagina()}_ranking_{id_produtos_promocoes}_hoje", "className"),
    Output(
        f"{id_pagina()}_ranking_{id_produtos_promocoes}_historico",
        "className",
    ),
    Input(f"{id_pagina()}_valor_{id_produtos_promocoes}_escolhido", "children"),
    State(f"{id_pagina()}_valor_{id_produtos_promocoes}_hoje", "children"),
    State(f"{id_pagina()}_valor_{id_produtos_promocoes}_historico", "children"),
)

id_marcas_promocoes = "marcas_promocoes"
clientside_callback(
    uteis_processamento.callback_ranking_direto_valores(),
    Output(
        f"{id_pagina()}_ranking_{id_marcas_promocoes}_escolhido",
        "className",
    ),
    Output(f"{id_pagina()}_ranking_{id_marcas_promocoes}_hoje", "className"),
    Output(
        f"{id_pagina()}_ranking_{id_marcas_promocoes}_historico",
        "className",
    ),
    Input(f"{id_pagina()}_valor_{id_marcas_promocoes}_escolhido", "children"),
    State(f"{id_pagina()}_valor_{id_marcas_promocoes}_hoje", "children"),
    State(f"{id_pagina()}_valor_{id_marcas_promocoes}_historico", "children"),
)

id_produtos_abaixo_200 = "produtos_abaixo_200"
clientside_callback(
    uteis_processamento.callback_ranking_direto_valores(),
    Output(
        f"{id_pagina()}_ranking_{id_produtos_abaixo_200}_escolhido",
        "className",
    ),
    Output(f"{id_pagina()}_ranking_{id_produtos_abaixo_200}_hoje", "className"),
    Output(
        f"{id_pagina()}_ranking_{id_produtos_abaixo_200}_historico",
        "className",
    ),
    Input(
        f"{id_pagina()}_valor_{id_produtos_abaixo_200}_escolhido",
        "children",
    ),
    State(f"{id_pagina()}_valor_{id_produtos_abaixo_200}_hoje", "children"),
    State(
        f"{id_pagina()}_valor_{id_produtos_abaixo_200}_historico",
        "children",
    ),
)


id_percentual_medio_desconto = "percentual_medio_desconto"
clientside_callback(
    uteis_processamento.callback_ranking_direto_valores(),
    Output(
        f"{id_pagina()}_ranking_{id_percentual_medio_desconto}_escolhido",
        "className",
    ),
    Output(
        f"{id_pagina()}_ranking_{id_percentual_medio_desconto}_hoje",
        "className",
    ),
    Output(
        f"{id_pagina()}_ranking_{id_percentual_medio_desconto}_historico",
        "className",
    ),
    Input(
        f"{id_pagina()}_valor_{id_percentual_medio_desconto}_escolhido",
        "children",
    ),
    State(
        f"{id_pagina()}_valor_{id_percentual_medio_desconto}_hoje",
        "children",
    ),
    State(
        f"{id_pagina()}_valor_{id_percentual_medio_desconto}_historico",
        "children",
    ),
)

id_media_precos = "media_precos"
clientside_callback(
    uteis_processamento.callback_ranking_inverso_valores(),
    Output(f"{id_pagina()}_ranking_{id_media_precos}_escolhido", "className"),
    Output(f"{id_pagina()}_ranking_{id_media_precos}_hoje", "className"),
    Output(f"{id_pagina()}_ranking_{id_media_precos}_historico", "className"),
    Input(f"{id_pagina()}_valor_{id_media_precos}_escolhido", "children"),
    State(f"{id_pagina()}_valor_{id_media_precos}_hoje", "children"),
    State(f"{id_pagina()}_valor_{id_media_precos}_historico", "children"),
)

id_produtos_20_avaliacoes = "produtos_20_avaliacoes"
clientside_callback(
    uteis_processamento.callback_ranking_direto_valores(),
    Output(
        f"{id_pagina()}_ranking_{id_produtos_20_avaliacoes}_escolhido",
        "className",
    ),
    Output(
        f"{id_pagina()}_ranking_{id_produtos_20_avaliacoes}_hoje",
        "className",
    ),
    Output(
        f"{id_pagina()}_ranking_{id_produtos_20_avaliacoes}_historico",
        "className",
    ),
    Input(
        f"{id_pagina()}_valor_{id_produtos_20_avaliacoes}_escolhido",
        "children",
    ),
    State(
        f"{id_pagina()}_valor_{id_produtos_20_avaliacoes}_hoje",
        "children",
    ),
    State(
        f"{id_pagina()}_valor_{id_produtos_20_avaliacoes}_historico",
        "children",
    ),
)

id_produtos_sem_avaliacoes = "produtos_sem_avaliacoes"
clientside_callback(
    uteis_processamento.callback_ranking_inverso_valores(),
    Output(
        f"{id_pagina()}_ranking_{id_produtos_sem_avaliacoes}_escolhido",
        "className",
    ),
    Output(
        f"{id_pagina()}_ranking_{id_produtos_sem_avaliacoes}_hoje",
        "className",
    ),
    Output(
        f"{id_pagina()}_ranking_{id_produtos_sem_avaliacoes}_historico",
        "className",
    ),
    Input(
        f"{id_pagina()}_valor_{id_produtos_sem_avaliacoes}_escolhido",
        "children",
    ),
    State(f"{id_pagina()}_valor_{id_produtos_sem_avaliacoes}_hoje", "children"),
    State(
        f"{id_pagina()}_valor_{id_produtos_sem_avaliacoes}_historico",
        "children",
    ),
)

id_produtos_nota_maior_4 = "produtos_nota_maior_4"
clientside_callback(
    uteis_processamento.callback_ranking_direto_valores(),
    Output(
        f"{id_pagina()}_ranking_{id_produtos_nota_maior_4}_escolhido",
        "className",
    ),
    Output(
        f"{id_pagina()}_ranking_{id_produtos_nota_maior_4}_hoje",
        "className",
    ),
    Output(
        f"{id_pagina()}_ranking_{id_produtos_nota_maior_4}_historico",
        "className",
    ),
    Input(
        f"{id_pagina()}_valor_{id_produtos_nota_maior_4}_escolhido",
        "children",
    ),
    State(f"{id_pagina()}_valor_{id_produtos_nota_maior_4}_hoje", "children"),
    State(
        f"{id_pagina()}_valor_{id_produtos_nota_maior_4}_historico",
        "children",
    ),
)
