from dash import html, register_page
from dash_ag_grid import AgGrid

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
