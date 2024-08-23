from dash import html, register_page
from dash_ag_grid import AgGrid

register_page(__name__, path="/pagina-2", name="Pagina 2", title="Pagina 2")


layout = html.Div(
    [
        html.H1("This is our Archive page"),
        html.Div("This is our Archive page content."),
        html.Button("Download CSV", id="csv-button", n_clicks=0),
        AgGrid(
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
