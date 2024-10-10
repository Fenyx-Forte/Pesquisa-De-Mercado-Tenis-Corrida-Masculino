import plotly.express as px
from dash import (
    dcc,
    html,
)
from dash_ag_grid import AgGrid
from dash_bootstrap_components import (
    Button,
    Modal,
    ModalBody,
    ModalHeader,
    ModalTitle,
)
from pandas import DataFrame as pd_DataFrame
from plotly.graph_objects import Figure

from dashboard.uteis import traducoes


def div_titulo(titulo: str) -> html.Div:
    conteudo = html.Div(
        html.H1(titulo, className="titulo-pagina"),
        className="titulo_pagina",
    )

    return conteudo


def seletor_datas(
    id_pagina: str,
    data_mais_antiga: str,
    data_mais_recente: str,
) -> dcc.DatePickerRange:
    conteudo = dcc.DatePickerRange(
        id=f"{id_pagina}_seletor_datas",
        start_date_placeholder_text="Data Inicial",
        end_date_placeholder_text="Data Final",
        display_format="DD/MM/YYYY",
        min_date_allowed=data_mais_antiga,
        max_date_allowed=data_mais_recente,
        clearable=True,
        minimum_nights=0,
        show_outside_days=False,
    )

    return conteudo


def botao_selecionar_periodo(id_pagina: str) -> Button:
    conteudo = Button(
        "Selecionar Período",
        outline=True,
        color="primary",
        className="me-1",
        id=f"{id_pagina}_botao",
        class_name="botao",
    )

    return conteudo


def div_seletor_datas_e_botao(
    id_pagina: str,
    data_mais_antiga: str,
    data_mais_recente: str,
) -> html.Div:
    conteudo = html.Div(
        [
            seletor_datas(id_pagina, data_mais_antiga, data_mais_recente),
            html.Br(),
            botao_selecionar_periodo(id_pagina),
        ],
        className="seletor_datas_e_botao",
    )

    return conteudo


def modal_erro(id_pagina: str) -> Modal:
    conteudo = Modal(
        [
            ModalHeader(
                ModalTitle("Titulo", id=f"{id_pagina}_modal_erro_titulo")
            ),
            ModalBody("Conteudo", id=f"{id_pagina}_modal_erro_conteudo"),
        ],
        id=f"{id_pagina}_modal_erro",
        is_open=False,
    )

    return conteudo


def cabecalho_coluna(
    id_pagina: str,
    sufixo_coluna: str,
    titulo: str,
    periodo: str,
) -> html.Div:
    conteudo = html.Div(
        [
            html.H4(
                titulo,
                className="titulo_coluna",
            ),
            html.Br(),
            html.H5(
                periodo,
                className="periodo_coluna",
                id=f"{id_pagina}_periodo_{sufixo_coluna}",
            ),
        ],
        className="cabecalho_coluna",
    )

    return conteudo


def conteiner_informacao(
    titulo_informacao: str,
    informacao: html.Div,
) -> html.Div:
    conteudo = html.Div(
        [
            html.H5(
                titulo_informacao,
                className="titulo_informacao",
            ),
            informacao,
        ],
        className="conteiner_informacao",
    )

    return conteudo


def figura_grafico_barras_simples(
    df: pd_DataFrame,
    coluna_x: str,
    coluna_y: str,
    cor: str,
    labels: dict[str, str],
    hover_data: dict,
) -> Figure:
    figura = (
        px.bar(
            df,
            x=coluna_x,
            y=coluna_y,
            labels=labels,
            color_discrete_sequence=[cor],
            barmode="group",
            hover_data=hover_data,
            text_auto=".2f",
        )
        .update_traces(
            textfont_size=12,
            # textangle=0,
            textfont_color="#000000",
            textposition="outside",
            # textposition="auto",
            cliponaxis=False,
        )
        .update_layout(
            dragmode=False,
            hoverlabel=dict(font_size=12, font_color="#FFFFFF"),
            uniformtext_minsize=10,
            uniformtext_mode="hide",
            showlegend=False,
        )
    )

    return figura


def figura_grafico_de_barras_agrupadas(
    df: pd_DataFrame,
    coluna_x: str,
    coluna_y: str,
    coluna_divisao: str,
    cores: list[str],
    labels: dict[str, str],
    hover_data: dict,
) -> Figure:
    # Cores que uso geralmente
    # #6495ED
    # #FFA07A
    # #5CB85C

    figura = (
        px.bar(
            df,
            x=coluna_x,
            y=coluna_y,
            labels=labels,
            color=coluna_divisao,
            color_discrete_sequence=cores,
            barmode="group",
            hover_data=hover_data,
            text_auto=".2f",
        )
        .update_traces(
            textfont_size=12,
            # textangle=0,
            textfont_color="#000000",
            textposition="outside",
            # textposition="auto",
            cliponaxis=False,
        )
        .update_layout(
            dragmode=False,
            hoverlabel=dict(font_size=12, font_color="#FFFFFF"),
            uniformtext_minsize=10,
            uniformtext_mode="hide",
            showlegend=False,
        )
    )

    return figura


def grafico_de_barras_simples(
    id_grafico: str,
    df: pd_DataFrame,
    coluna_x: str,
    coluna_y: str,
    cor: str,
    labels: dict[str, str],
    hover_data: dict,
) -> dcc.Graph:
    figura = figura_grafico_barras_simples(
        df=df,
        coluna_x=coluna_x,
        coluna_y=coluna_y,
        cor=cor,
        labels=labels,
        hover_data=hover_data,
    )

    grafico = dcc.Graph(
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

    return grafico


def grafico_de_barras_agrupadas(
    id_grafico: str,
    df: pd_DataFrame,
    coluna_x: str,
    coluna_y: str,
    coluna_divisao: str,
    cores: list[str],
    labels: dict[str, str],
    hover_data: dict,
) -> dcc.Graph:
    figura = figura_grafico_de_barras_agrupadas(
        df=df,
        coluna_x=coluna_x,
        coluna_y=coluna_y,
        coluna_divisao=coluna_divisao,
        cores=cores,
        labels=labels,
        hover_data=hover_data,
    )

    grafico = dcc.Graph(
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

    return grafico


def tabela_ag_grid(
    dados: list[dict], id_completo: str, definicoes_colunas: list[dict]
) -> AgGrid:
    conteudo = AgGrid(
        rowData=dados,
        id=id_completo,
        columnDefs=definicoes_colunas,
        columnSize="responsiveSizeToFit",
        defaultColDef={
            "resizable": False,
            "filter": True,
            "headerClass": "center-aligned-header",
            "cellClass": "center-aligned-cell",
            "wrapHeaderText": True,
            "autoHeaderHeight": True,
            "wrapText": True,
            "autoHeight": True,
            "cellStyle": {
                "wordBreak": "normal",
                "lineHeight": "unset",
            },
            "suppressMovable": True,
        },
        dashGridOptions={
            "animateRows": False,
            "suppressColumnMoveAnimation": True,
            "suppressDragLeaveHidesColumns": True,
            "suppressMenuHide": True,
            "pagination": False,
            "tooltipShowDelay": 500,
            "alwaysMultiSort": True,
            "enableBrowserTooltips": True,
            "localeText": traducoes.dag_locale_pt_br(),
        },
        className="ag-theme-quartz tabela-ag-grid",
    )

    return conteudo
