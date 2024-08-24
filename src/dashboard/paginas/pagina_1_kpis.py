from dash import html, register_page

register_page(
    __name__,
    path="/kpis",
    name="KPI's",
    title="KPI's",
    description="KPI's",
    image="logo.png",
)


layout = html.Div(
    [
        html.H1("This is our Analytics page"),
        html.Div("This is our Analytics page content."),
    ],
    className="pagina",
)
