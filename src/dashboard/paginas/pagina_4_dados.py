from dash import (
    Input,
    Output,
    callback,
    clientside_callback,
    html,
    register_page,
)
from dash_ag_grid import AgGrid
from dash_bootstrap_components import Button

from dashboard.processamento import gerenciador
from dashboard.uteis import formatacoes, traducoes

register_page(
    __name__,
    path="/dados",
    name="Dados",
    title="Dados",
    description="Página Dados",
    image_url="/assets/images/imagem_link.jpg",
)


def titulo() -> html.H1:
    conteudo = html.H1("Página Dados")

    return conteudo


def botao_exportar_csv() -> Button:
    conteudo = Button(
        "Exportar CSV",
        outline=True,
        color="primary",
        className="me-1",
        id="botao-exportar-csv",
    )

    return conteudo


def configuracoes_colunas_tabela_dados() -> list[dict]:
    configuracoes = [
        {
            "headerName": "Marca",
            "field": "marca",
            "headerTooltip": "Marca tênis",
            "cellDataType": "text",
        },
        {
            "headerName": "Produto",
            "field": "produto",
            "headerTooltip": "Tênis",
            "cellDataType": "text",
        },
        {
            "headerName": "Preço Atual",
            "field": "preco_atual",
            "headerTooltip": "Preço tênis",
            "cellDataType": "number",
            "valueFormatter": {
                "function": f"{formatacoes.dag_format_pt_br()}.format('$,.2f')(params.value)",
            },
        },
        {
            "headerName": "Promoção?",
            "field": "promocao",
            "headerTooltip": "Tênis em Promoção",
            "cellDataType": "boolean",
        },
        {
            "headerName": "Desconto",
            "field": "percentual_promocao",
            "headerTooltip": "Desconto tênis",
            "cellDataType": "number",
            "valueFormatter": {
                "function": f"{formatacoes.dag_format_pt_br()}.format(',.2%')(params.value)",
            },
        },
    ]

    return configuracoes


def tabela_dados() -> AgGrid:
    conteudo = AgGrid(
        rowData=gerenciador.pagina_4_inicializa_tabela(),
        id="tabela-dados",
        columnDefs=configuracoes_colunas_tabela_dados(),
        defaultColDef={
            "resizable": True,
            "filter": True,
            "headerClass": "center-aligned-header",
            "cellClass": "center-aligned-cell",
            "wrapHeaderText": True,
            "autoHeaderHeight": True,
        },
        dashGridOptions={
            "animateRows": False,
            "suppressColumnMoveAnimation": True,
            "pagination": True,
            "tooltipShowDelay": 500,
            "alwaysMultiSort": True,
            "localeText": traducoes.dag_locale_pt_br(),
        },
        columnSize="responsiveSizeToFit",
        csvExportParams={
            "fileName": "tabela_dados.csv",
        },
        className="ag-theme-quartz meu-dag",
    )

    return conteudo


layout = html.Div(
    [
        titulo(),
        html.Br(),
        botao_exportar_csv(),
        html.Br(),
        html.Br(),
        tabela_dados(),
    ],
    className="pagina",
)


clientside_callback(
    """
    function(nClicks) {
        if (nClicks) {
            return true;
        }
        return false;
    }
    """,
    Output("tabela-dados", "exportDataAsCsv"),
    Input("botao-exportar-csv", "n_clicks"),
    prevent_initial_call=True,
)
