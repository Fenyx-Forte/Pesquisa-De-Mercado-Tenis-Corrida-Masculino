from dash import html, register_page
from dash_ag_grid import AgGrid

register_page(
    __name__,
    path="/promocoes",
    name="Promoções",
    title="Promoções",
    description="Promoções",
    image="logo.png",
)


layout = html.Div(
    [
        html.H1("This is our Promoções page"),
        html.Div("This is our Promoções page content."),
    ],
    className="pagina",
)
