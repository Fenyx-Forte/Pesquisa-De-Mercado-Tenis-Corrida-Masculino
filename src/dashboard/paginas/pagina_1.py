from dash import html, register_page

register_page(__name__, path="/pagina-1", name="Pagina 1", title="Pagina 1")


layout = html.Div(
    [
        html.H1("This is our Analytics page"),
        html.Div("This is our Analytics page content."),
    ],
    className="pagina",
)
