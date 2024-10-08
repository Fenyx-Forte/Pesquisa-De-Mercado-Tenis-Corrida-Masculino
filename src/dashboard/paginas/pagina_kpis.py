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
    image_url="https://analise-de-dados-mercadolivre.onrender.com/assets/images/imagem_link.jpg",
)


def id_pagina() -> str:
    return "kpis"


def titulo_pagina() -> str:
    return "KPI's Principais"


def informacao(
    valor: str,
    id_informacao: str,
    sufixo_coluna: str,
) -> html.Div:
    conteudo = html.Div(
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

    return conteudo


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
    conteudo = html.Div(
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
                titulo_informacao="Média Preços (R$)",
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
                titulo_informacao="Produtos Em Promocão",
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
                titulo_informacao="Média Desconto (%)",
                informacao=informacao(
                    valor=percentual_medio_desconto,
                    sufixo_coluna=sufixo_coluna,
                    id_informacao="percentual_medio_desconto",
                ),
            ),
        ],
    )

    return conteudo


def colunas() -> Row:
    periodo_hoje = gerenciador.retorna_periodo_hoje()

    periodo_escolhido = gerenciador.retorna_periodo_ultima_semana()

    periodo_historico = gerenciador.retorna_periodo_historico()

    dados_hoje = gerenciador.pagina_kpis_dados_hoje()

    dados_escolhido = gerenciador.pagina_kpis_dados_ultima_semana()

    dados_historico = gerenciador.pagina_kpis_dados_historico()

    conteudo = Row(
        [
            Col(
                coluna(
                    sufixo_coluna="hoje",
                    titulo_cabecalho="Hoje",
                    periodo=periodo_hoje,
                    **dados_hoje,
                ),
                width=4,
                class_name="coluna_hoje",
            ),
            Col(
                coluna(
                    sufixo_coluna="escolhido",
                    titulo_cabecalho="Período Escolhido",
                    periodo=periodo_escolhido,
                    **dados_escolhido,
                ),
                width=4,
                class_name="coluna_escolhido",
            ),
            Col(
                coluna(
                    sufixo_coluna="historico",
                    titulo_cabecalho="Histórico",
                    periodo=periodo_historico,
                    **dados_historico,
                ),
                width=4,
                class_name="coluna_historico",
            ),
        ],
        class_name="linha_colunas",
    )

    return conteudo


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
        f"{id_pagina()}_valor_produtos_sem_avaliacoes_escolhido", "children"
    ),
    Output(f"{id_pagina()}_valor_produtos_promocoes_escolhido", "children"),
    Output(
        f"{id_pagina()}_valor_marcas_promocoes_escolhido",
        "children",
    ),
    Output(
        f"{id_pagina()}_valor_percentual_medio_desconto_escolhido", "children"
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
def kpis_atualizar_dados_escolhido(titulo, data_inicio, data_fim):
    if titulo != "":
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
        f"{id_pagina()}_ranking_{id_produtos_promocoes}_escolhido", "className"
    ),
    Output(f"{id_pagina()}_ranking_{id_produtos_promocoes}_hoje", "className"),
    Output(
        f"{id_pagina()}_ranking_{id_produtos_promocoes}_historico", "className"
    ),
    Input(f"{id_pagina()}_valor_{id_produtos_promocoes}_escolhido", "children"),
    State(f"{id_pagina()}_valor_{id_produtos_promocoes}_hoje", "children"),
    State(f"{id_pagina()}_valor_{id_produtos_promocoes}_historico", "children"),
)

id_marcas_promocoes = "marcas_promocoes"
clientside_callback(
    uteis_processamento.callback_ranking_direto_valores(),
    Output(
        f"{id_pagina()}_ranking_{id_marcas_promocoes}_escolhido", "className"
    ),
    Output(f"{id_pagina()}_ranking_{id_marcas_promocoes}_hoje", "className"),
    Output(
        f"{id_pagina()}_ranking_{id_marcas_promocoes}_historico", "className"
    ),
    Input(f"{id_pagina()}_valor_{id_marcas_promocoes}_escolhido", "children"),
    State(f"{id_pagina()}_valor_{id_marcas_promocoes}_hoje", "children"),
    State(f"{id_pagina()}_valor_{id_marcas_promocoes}_historico", "children"),
)

id_produtos_abaixo_200 = "produtos_abaixo_200"
clientside_callback(
    uteis_processamento.callback_ranking_direto_valores(),
    Output(
        f"{id_pagina()}_ranking_{id_produtos_abaixo_200}_escolhido", "className"
    ),
    Output(f"{id_pagina()}_ranking_{id_produtos_abaixo_200}_hoje", "className"),
    Output(
        f"{id_pagina()}_ranking_{id_produtos_abaixo_200}_historico", "className"
    ),
    Input(
        f"{id_pagina()}_valor_{id_produtos_abaixo_200}_escolhido", "children"
    ),
    State(f"{id_pagina()}_valor_{id_produtos_abaixo_200}_hoje", "children"),
    State(
        f"{id_pagina()}_valor_{id_produtos_abaixo_200}_historico", "children"
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
        f"{id_pagina()}_valor_{id_percentual_medio_desconto}_hoje", "children"
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
        f"{id_pagina()}_ranking_{id_produtos_sem_avaliacoes}_hoje", "className"
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
        f"{id_pagina()}_ranking_{id_produtos_nota_maior_4}_hoje", "className"
    ),
    Output(
        f"{id_pagina()}_ranking_{id_produtos_nota_maior_4}_historico",
        "className",
    ),
    Input(
        f"{id_pagina()}_valor_{id_produtos_nota_maior_4}_escolhido", "children"
    ),
    State(f"{id_pagina()}_valor_{id_produtos_nota_maior_4}_hoje", "children"),
    State(
        f"{id_pagina()}_valor_{id_produtos_nota_maior_4}_historico", "children"
    ),
)
