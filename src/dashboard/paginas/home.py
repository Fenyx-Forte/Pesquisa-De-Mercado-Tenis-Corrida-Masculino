from dash import html, register_page

register_page(
    __name__,
    path="/",
    name="Home",
    title="Home",
    description="Home",
    image="logo.png",
)


layout = html.Div(
    [
        html.H1("This is our Home page"),
        html.Div("This is our Home page content."),
    ],
    className="pagina",
)
