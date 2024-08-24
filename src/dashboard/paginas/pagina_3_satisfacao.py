from dash import html, register_page

register_page(
    __name__,
    path="/satisfacao",
    name="Satisfação",
    title="Satisfação",
    description="Satisfação",
    image="logo.png",
)


layout = html.Div(
    [
        html.H1("This is our Satisfação page"),
        html.Div("This is our Satisfação page content."),
    ],
    className="pagina",
)
