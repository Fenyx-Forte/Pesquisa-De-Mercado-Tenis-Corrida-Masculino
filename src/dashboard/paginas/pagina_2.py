import dash
import dash_ag_grid as dag
from dash import Input, Output, callback, html

dash.register_page(
    __name__, path="/pagina-2", name="Pagina 2", title="Pagina 2"
)


def layout(**kwargs) -> html.Div:
    conteudo = html.Div(
        [
            html.H1("This is our Archive page"),
            html.Div("This is our Archive page content."),
            html.Button("Download CSV", id="csv-button", n_clicks=0),
            dag.AgGrid(
                id="meu-dag",
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
                    "pagination": True,
                    "tooltipShowDelay": 500,
                    "alwaysMultiSort": True,
                },
                columnSize="sizeToFit",
                csvExportParams={
                    "fileName": "ag_grid_test.csv",
                },
                className="ag-theme-quartz meu-dag",
            ),
        ],
        className="pagina",
    )

    return conteudo


@callback(
    Output("meu-dag", "exportDataAsCsv"),
    Input("csv-button", "n_clicks"),
)
def export_data_as_csv(n_clicks):
    if n_clicks:
        return True
    return False


@callback(
    Output("meu-dag", "rowData"),
    Output("meu-dag", "columnDefs"),
    Input("store", "data"),
)
def preencher_tabela(store):
    colunas = [
        {
            "headerName": "Marca",
            "field": "marca",
            "headerTooltip": "Marca do tênis",
        },
        {
            "headerName": "Preço",
            "field": "preco_atual",
            "headerTooltip": "Preço do tênis",
        },
    ]

    return store["df"], colunas
