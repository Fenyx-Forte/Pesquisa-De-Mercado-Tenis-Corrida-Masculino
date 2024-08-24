from dash import html, register_page
from dash_ag_grid import AgGrid
from dashboard import formatacoes, traducoes

register_page(
    __name__,
    path="/dados",
    name="Dados",
    title="Dados",
    description="Dados",
    image="logo.png",
)


layout = html.Div(
    [
        html.H1("This is our Dados page"),
        html.Div("This is our Dados page content."),
        html.Br(),
        html.Button("Download CSV", id="csv-button", n_clicks=0),
        AgGrid(
            id="meu-dag",
            columnDefs=[
                {
                    "headerName": "Marca",
                    "field": "marca",
                    "headerTooltip": "Marca do tênis",
                    "cellDataType": "text",
                },
                {
                    "headerName": "Preço",
                    "field": "preco_atual",
                    "headerTooltip": "Preço do tênis",
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
                    "headerTooltip": "Desconto do tênis",
                    "cellDataType": "number",
                    "valueFormatter": {
                        "function": f"{formatacoes.dag_format_pt_br()}.format(',.2%')(params.value)",
                    },
                },
            ],
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
                "fileName": "ag_grid_test.csv",
            },
            className="ag-theme-quartz meu-dag",
        ),
    ],
    className="pagina",
)
