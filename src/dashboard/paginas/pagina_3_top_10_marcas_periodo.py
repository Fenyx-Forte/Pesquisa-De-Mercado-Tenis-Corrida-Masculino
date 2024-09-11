import plotly.express as px
from dash import (
    Input,
    Output,
    State,
    callback,
    clientside_callback,
    dcc,
    html,
    register_page,
)
from dash.exceptions import PreventUpdate
from dash_bootstrap_components import (
    Button,
    Modal,
    ModalBody,
    ModalHeader,
    ModalTitle,
)
from pandas import DataFrame as pd_DataFrame

from dashboard.processamento import gerenciador

register_page(
    __name__,
    path="/top-10-marcas-periodo",
    name="Top 10 Marcas Período",
    title="Top 10 Marcas Período",
    description="Top 10 Marcas Período",
    image_url="/assets/images/imagem_link.jpg",
)


def titulo() -> html.H1:
    conteudo = html.H1("Top 10 Marcas Período")

    return conteudo


def seletor_datas() -> dcc.DatePickerRange:
    conteudo = dcc.DatePickerRange(
        id="pagina_3_seletor_datas",
        start_date_placeholder_text="Data Inicial",
        end_date_placeholder_text="Data Final",
        display_format="DD/MM/YYYY",
        min_date_allowed=gerenciador.retorna_data_coleta_mais_antiga(),
        max_date_allowed=gerenciador.retorna_data_coleta_mais_recente(),
        clearable=True,
        minimum_nights=0,
        show_outside_days=False,
    )

    return conteudo


def botao_adicionar_periodo() -> Button:
    conteudo = Button(
        "Adicionar Período",
        outline=True,
        color="primary",
        className="me-1",
        id="pagina_3_botao",
    )

    return conteudo


def modal_erro() -> Modal:
    conteudo = Modal(
        [
            ModalHeader(ModalTitle("Titulo", id="pagina_3_modal_erro_titulo")),
            ModalBody("Conteudo", id="pagina_3_modal_erro_conteudo"),
        ],
        id="pagina_3_modal_erro",
        is_open=False,
    )

    return conteudo


def figura_top_10_marcas(df: pd_DataFrame, cor: str) -> px.bar:
    figura = (
        px.bar(
            df,
            x="Marca",
            y="Porcentagem",
            color="Periodo",
            labels={"Periodo": "Período"},
            color_discrete_sequence=[cor],
            barmode="group",
            hover_data={
                "Porcentagem": ":.2f",
                "Periodo": False,
                "Marca": False,
            },
            text_auto=".2f",
        )
        .update_traces(
            textfont_size=12,
            textangle=0,
            textfont_color="#000000",
            textposition="outside",
            cliponaxis=False,
            # textposition="auto",
        )
        .update_layout(
            dragmode=False,
            hoverlabel=dict(font_size=12, font_color="#FFFFFF"),
            uniformtext_minsize=10,
            uniformtext_mode="hide",
            legend=dict(
                font=dict(size=14, color="black"),
            ),
        )
    )

    return figura


def grafico_top_10_marcas(
    df: pd_DataFrame, cor: str, id_grafico: str
) -> dcc.Graph:
    figura = figura_top_10_marcas(df, cor)

    conteudo = dcc.Graph(
        figure=figura,
        responsive=True,
        config={
            "displayModeBar": False,
            "doubleClick": False,
            "editSelection": False,
            "editable": False,
            "scrollZoom": False,
            "showTips": False,
        },
        id=id_grafico,
    )

    return conteudo


layout = html.Div(
    [
        # titulo(),
        # html.Br(),
        seletor_datas(),
        botao_adicionar_periodo(),
        modal_erro(),
        grafico_top_10_marcas(
            gerenciador.pagina_3_top_10_marcas_historico(),
            "#6495ED",
            "grafico-top-10-marcas-1",
        ),
        html.Div("", id="pagina_3_div_grafico_2"),
        html.Div("", id="pagina_3_div_grafico_3"),
    ],
    className="pagina",
    id="pagina_3",
)


clientside_callback(
    """
    function limparSeletorDatas(n_clicks, data_inicio, data_fim) {
        if (data_inicio === null || data_fim === null) {
            return window.dash_clientside.no_update;
        }
        return [null, null];
    }
    """,
    Output("pagina_3_seletor_datas", "start_date"),
    Output("pagina_3_seletor_datas", "end_date"),
    Input("pagina_3_botao", "n_clicks"),
    State("pagina_3_seletor_datas", "start_date"),
    State("pagina_3_seletor_datas", "end_date"),
    prevent_initial_call=True,
)


@callback(
    Output("pagina_3_div_grafico_2", "children"),
    Input("pagina_3_botao", "n_clicks"),
    State("pagina_3_seletor_datas", "start_date"),
    State("pagina_3_seletor_datas", "end_date"),
    State("pagina_3_div_grafico_2", "children"),
    prevent_initial_call=True,
)
def adicionar_grafico_2(n_clicks, data_inicio, data_fim, conteudo_div_2):
    if data_inicio is None:
        raise PreventUpdate
    if data_fim is None:
        raise PreventUpdate

    if conteudo_div_2 != "":
        raise PreventUpdate

    dados_grafico = gerenciador.pagina_3_top_10_marcas_periodo(
        data_inicio, data_fim
    )

    return grafico_top_10_marcas(
        dados_grafico, "#FFA07A", "grafico-top-10-marcas-2"
    )


@callback(
    Output("pagina_3_div_grafico_3", "children"),
    Input("pagina_3_botao", "n_clicks"),
    State("pagina_3_seletor_datas", "start_date"),
    State("pagina_3_seletor_datas", "end_date"),
    State("pagina_3_div_grafico_2", "children"),
    State("pagina_3_div_grafico_3", "children"),
    prevent_initial_call=True,
)
def adicionar_grafico_3(
    n_clicks, data_inicio, data_fim, conteudo_div_2, conteudo_div_3
):
    if data_inicio is None:
        raise PreventUpdate
    if data_fim is None:
        raise PreventUpdate

    if conteudo_div_2 == "":
        raise PreventUpdate

    if conteudo_div_3 != "":
        raise PreventUpdate

    dados_grafico = gerenciador.pagina_3_top_10_marcas_periodo(
        data_inicio, data_fim
    )

    return grafico_top_10_marcas(
        dados_grafico, "#5CB85C", "grafico-top-10-marcas-3"
    )
